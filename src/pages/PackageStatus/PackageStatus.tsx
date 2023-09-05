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
  Checkbox,
  Table,
  TableContainer,
  Tbody,
  Td,
  Th,
  Thead,
  Tr,
  Select,
  Button,
} from "@chakra-ui/react";

import {
  ArrowUpIcon,
  ArrowDownIcon,
  TimeIcon,
  CheckIcon,
} from "@chakra-ui/icons";
import ConfirmPackagesModal from "../../components/ConfirmPackagesModal/ConfirmPackagesModal";
import "./PackageStatus.css";

const PackageStatus = () => {
  const [packages, setPackages] = useState<any>([]);
  const [loading, setLoading] = useState(true);
  const [collectedPackages, setCollectedPackages] = useState<string[]>([]);
  const [order, setOrder] = useState("");
  const [focusedColumn, setFocusedColumn] = useState("");
  const [search, setSearch] = useState("");
  const [filterOption, setFilterOption] = useState("");
  const [toggleCollectedView, setToggleCollectedView] = useState(false);

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
      <div className="title">
        <Text as="b" fontSize="4xl">
          Package Status
        </Text>
      </div>
      <div className="search-filter">
        <Input
          placeholder="Search"
          width="200px"
          onChange={(e) => setSearch(e.target.value)}
          isDisabled={filterOption === ""}
        />
        <Select
          width="200px"
          placeholder="Filter by..."
          onChange={(e) => setFilterOption(e.target.value)}
        >
          <option value="trackingNumber">Tracking Number</option>
          <option value="mailboxNumber">Mailbox Number</option>
          <option value="customer">Customer</option>
          <option value="dateScanned">Date Scanned</option>
          <option value="status">Status</option>
        </Select>
        <Button onClick={() => setToggleCollectedView(!toggleCollectedView)}>
          {toggleCollectedView ? "Hide" : "Show"} Collected Packages
        </Button>
      </div>
      <div className="packages-table">
        <TableContainer overflowY="auto" maxHeight="275px" w="100%">
          <Table variant="simple">
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
                packages
                  .filter((p: any) => {
                    return search.toLowerCase() === ""
                      ? p
                      : p[filterOption].toLowerCase().includes(search);
                  })
                  .filter((p: any) => {
                    return toggleCollectedView == false
                      ? p["status"].includes("Pending")
                      : p;
                  })
                  .map((p: any) => (
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
                  <Td>No packages to display.</Td>
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

export default PackageStatus;
