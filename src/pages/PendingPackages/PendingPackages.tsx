import { useState, useEffect } from "react";
import {
  doc,
  getDocs,
  updateDoc,
  collection,
  onSnapshot,
  query,
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
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  useDisclosure,
} from "@chakra-ui/react";
import "./PendingPackages.css";

const PendingPackages = () => {
  const [packages, setPackages] = useState<any>([]);
  const [loading, setLoading] = useState(true);
  const [collectedPackages, setCollectedPackages] = useState<string[]>([]);
  const [showCollected, setShowCollected] = useState(false);

  const { isOpen, onOpen, onClose } = useDisclosure();

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
      updateDoc(doc(db, "pending-packages", p), { status: "Collected" });
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

    onClose();
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
                <Th>Tracking Number</Th>
                <Th>Mailbox Number</Th>
                <Th>Customer</Th>
                <Th>Date Scanned</Th>
                <Th>Status</Th>
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
                      {p.status == "Pending" && (
                        <Checkbox
                          className="checkbox"
                          onChange={() => modifyCollectedPackages(p.key)}
                        />
                      )}
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
      <Button isDisabled={collectedPackages.length == 0} onClick={onOpen}>
        Confirm Collected Packages
      </Button>
      <Button onClick={() => setShowCollected(!showCollected)}>
        Show Collected Packages
      </Button>

      <Modal isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Confirm Package Collection</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <Text>
              Please confirm that the packages have been picked up and are no
              longer pending/in-store. Confirming will mark the selected
              packages from "Pending" to "Collected".
            </Text>
          </ModalBody>

          <ModalFooter>
            <Button colorScheme="blue" mr={3} onClick={onClose}>
              Close
            </Button>
            <Button colorScheme="green" onClick={confirmPendingPackages}>
              Confirm Package Collection
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  );
};

export default PendingPackages;
