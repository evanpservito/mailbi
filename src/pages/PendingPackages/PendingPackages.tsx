import { useState, useEffect } from "react";
import {
  doc,
  getDocs,
  updateDoc,
  collection,
  onSnapshot,
  query,
  Timestamp,
} from "firebase/firestore";

import firebase from "../../Firebase";
import db from "../../Firebase";
import {
  Text,
  Input,
  Button,
  Checkbox,
  Table,
  TableContainer,
  Tbody,
  Td,
  Th,
  Thead,
  Tr,
  useDisclosure,
} from "@chakra-ui/react";

import {
  ArrowUpIcon,
  ArrowDownIcon,
  TimeIcon,
  CheckIcon,
} from "@chakra-ui/icons";
import ConfirmPackagesModal from "../../components/ConfirmPackagesModal/ConfirmPackagesModal";
import "./PendingPackages.css";

const PendingPackages = () => {
  const [packages, setPackages] = useState<any>([]);
  const [loading, setLoading] = useState(true);
  const [collectedPackages, setCollectedPackages] = useState<string[]>([]);
  const [showCollected, setShowCollected] = useState(false);
  const [order, setOrder] = useState("");
  const [focusedColumn, setFocusedColumn] = useState("");

  // Get pending packages from Firebase
  useEffect(() => {
    const firebasePackages: any[] = [];
    const q = query(collection(firebase, "pending-packages"));
    const unsub = onSnapshot(q, (querySnapshot) => {
      querySnapshot.forEach((doc) => {
        firebasePackages.push({
          ...doc.data(),
          key: doc.id,
        });
      });
      setPackages(firebasePackages);
      // console.log(firebasePackages);
      setLoading(false);
    });

    return () => {
      unsub();
    };
  }, [loading]);

  if (loading) {
    <Text>Loading Data...</Text>;
  }

  const modifyCollectedPackages = (packageKey: string) => {
    if (collectedPackages.includes(packageKey)) {
      setCollectedPackages((collectedPackages) =>
        collectedPackages.filter((p: any) => p != packageKey)
      );
    } else {
      setCollectedPackages([...collectedPackages, packageKey]);
    }
  };

  const confirmPendingPackages = async () => {
    await collectedPackages.forEach((p: any) => {
      updateDoc(doc(db, "pending-packages", p), {
        status: "Collected",
        dateCollected: Timestamp.fromDate(new Date()),
      });

      modifyCollectedPackages(p);
    });

    // update table
    const firebasePackages: any[] = [];
    const q = query(collection(firebase, "pending-packages"));
    const querySnapshot = await getDocs(q);
    querySnapshot.forEach((doc: any) => {
      firebasePackages.push({
        ...doc.data(),
        key: doc.id,
      });
      setPackages(firebasePackages);
    });
  };

  const timeStampToDate = (date: any) => {
    const newDate = new Timestamp(date.seconds, date.nanoseconds).toDate();

    return (
      newDate.getMonth() +
      1 +
      "/" +
      newDate.getDate() +
      "/" +
      newDate.getFullYear()
    );
  };

  const sortPackages = (column: string) => {
    if (order === "ASC" || order === "") {
      const sortedPackages = [...packages].sort((a, b) =>
        a[column].toLowerCase() > b[column].toLowerCase() ? 1 : -1
      );
      setPackages(sortedPackages);
      setOrder("DSC");
    } else if (order === "DSC" || order === "") {
      const sortedPackages = [...packages].sort((a, b) =>
        a[column].toLowerCase() < b[column].toLowerCase() ? 1 : -1
      );
      setPackages(sortedPackages);
      setOrder("ASC");
    }
    setFocusedColumn(column);
  };

  return (
    <>
      <Text as="b" fontSize="4xl">
        Pending Packages
      </Text>
      <div className="packages-table">
        <TableContainer overflowY="auto" maxHeight="275px">
          <Input placeholder="Filter" width="200px" />
          <Table variant="simple" width="1000px">
            <Thead
              className="table-head"
              position="sticky"
              top={0}
              bgColor="#b5e3eb"
            >
              <Tr>
                <Th
                  cursor="pointer"
                  onClick={() => sortPackages("trackingNumber")}
                >
                  Tracking Number{" "}
                  {focusedColumn === "trackingNumber" &&
                    ((order === "ASC" && <ArrowUpIcon />) ||
                      (order === "DSC" && <ArrowDownIcon />))}
                </Th>
                <Th
                  cursor="pointer"
                  onClick={() => sortPackages("mailboxNumber")}
                >
                  Mailbox Number{" "}
                  {focusedColumn === "mailboxNumber" &&
                    ((order === "ASC" && <ArrowUpIcon />) ||
                      (order === "DSC" && <ArrowDownIcon />))}
                </Th>
                <Th cursor="pointer" onClick={() => sortPackages("customer")}>
                  Customer{" "}
                  {focusedColumn === "customer" &&
                    ((order === "ASC" && <ArrowUpIcon />) ||
                      (order === "DSC" && <ArrowDownIcon />))}
                </Th>
                <Th
                  cursor="pointer"
                  onClick={() => sortPackages("dateScanned")}
                >
                  Date Scanned{" "}
                  {focusedColumn === "dateScanned" &&
                    ((order === "ASC" && <ArrowUpIcon />) ||
                      (order === "DSC" && <ArrowDownIcon />))}
                </Th>
                <Th cursor="pointer" onClick={() => sortPackages("status")}>
                  Status{" "}
                  {focusedColumn === "status" &&
                    ((order === "ASC" && <TimeIcon />) ||
                      (order === "DSC" && <CheckIcon />))}
                </Th>
                <Th>Collected</Th>
              </Tr>
            </Thead>
            <Tbody>
              {packages.length > 0 ? (
                packages.map((p: any) => (
                  <Tr key={p.key}>
                    <Td>{p.trackingNumber}</Td>
                    <Td>{p.mailboxNumber}</Td>
                    <Td>{p.customer}</Td>
                    <Td>{p.dateScanned}</Td>
                    <Td color={p.status == "Pending" ? "#cc9e12" : "green"}>
                      {p.status}
                    </Td>
                    <Td>
                      {(p.status == "Pending" && (
                        <Checkbox
                          className="checkbox"
                          onChange={() => modifyCollectedPackages(p.key)}
                        />
                      )) ||
                        (p.status == "Collected" &&
                          timeStampToDate(p.dateCollected))}
                    </Td>
                  </Tr>
                ))
              ) : (
                <Tr>
                  <Td>N/A</Td>
                </Tr>
              )}
            </Tbody>
          </Table>
        </TableContainer>
      </div>
      <ConfirmPackagesModal
        confirmPendingPackages={confirmPendingPackages}
        numPackages={collectedPackages.length}
      />
    </>
  );
};

export default PendingPackages;
