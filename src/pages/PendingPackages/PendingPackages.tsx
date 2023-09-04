import { useState, useEffect } from "react";
import { collection, onSnapshot, query } from "firebase/firestore";
import firebase from "../../Firebase";
import {
  Text,
  Button,
  Checkbox,
  Table,
  TableContainer,
  Tbody,
  Td,
  Th,
  Thead,
  Tr,
} from "@chakra-ui/react";
import "./PendingPackages.css";

const PendingPackages = () => {
  const [packages, setPackages] = useState<any>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const firebasePackages: any[] = [];
    const unsub = onSnapshot(
      query(collection(firebase, "pending-packages")),
      (querySnapshot) => {
        querySnapshot.forEach((doc) => {
          firebasePackages.push({
            ...doc.data(),
            key: doc.id,
          });
        });
        setPackages(firebasePackages);
        setLoading(false);
      }
    );

    return () => unsub();
  }, []);

  if (loading) {
    <Text>Loading Data...</Text>;
  }

  return (
    <div>
      <Text as="b" fontSize="4xl">
        Pending Packages
      </Text>
      <div className="packages-table">
        <TableContainer>
          <Table variant="simple" width="1000px">
            <Thead>
              <Tr>
                <Th>Tracking Number</Th>
                <Th>Mailbox Number</Th>
                <Th>Customer</Th>
                <Th>Date Scanned</Th>
                <Th>Picked Up</Th>
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
                    <Td>
                      <Checkbox />
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
      <Button>Remove Selected Packages</Button>
    </div>
  );
};

export default PendingPackages;
