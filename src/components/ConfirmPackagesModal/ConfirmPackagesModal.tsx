import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalCloseButton,
  ModalBody,
  ModalFooter,
  Button,
  Text,
  useDisclosure,
} from "@chakra-ui/react";

/* TODO: fix typescript "any" here */
const ConfirmPackagesModal = ({ confirmPendingPackages, numPackages }: any) => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  return (
    <>
      <Button isDisabled={numPackages == 0} onClick={onOpen}>
        Confirm Collected Packages
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
            <Button
              colorScheme="green"
              onClick={() => {
                confirmPendingPackages();
                onClose();
              }}
            >
              Confirm Package Collection
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  );
};
export default ConfirmPackagesModal;
