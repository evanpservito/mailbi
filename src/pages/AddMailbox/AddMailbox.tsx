import { useState } from "react";
import {
  Text,
  HStack,
  FormControl,
  FormLabel,
  NumberInput,
  NumberInputField,
  NumberInputStepper,
  NumberIncrementStepper,
  NumberDecrementStepper,
  Button,
  Input,
} from "@chakra-ui/react";
import firebase from "../../Firebase";
import db from "../../Firebase";
import {
  onSnapshot,
  collection,
  query,
  where,
  doc,
  updateDoc,
} from "firebase/firestore";
import "./AddMailbox.css";

const AddMailbox = () => {
  const [mailboxNumber, setMailboxNumber] = useState("");
  const [customer, setCustomer] = useState("");
  const [phoneNumber, setPhoneNumber] = useState("");
  const [validMailbox, setValidMailbox] = useState(false);
  const [existingMailboxCustomer, setExistingMailboxCustomer] = useState("");
  const [existingMailboxPhoneNumber, setExistingMailboxPhoneNumber] =
    useState("");
  const [submitMailbox, setSubmitMailbox] = useState(false);
  const [mailboxID, setMailboxID] = useState("");

  const checkEmptyMailbox = (e: any) => {
    const q = query(
      collection(firebase, "users"),
      where("mailboxNumber", "==", parseInt(e, 10))
    );

    const unsub = onSnapshot(q, (querySnapshot) => {
      const items: any[] = [];
      querySnapshot.forEach((doc) => {
        setMailboxID(doc.id);
        items.push(doc.data());
      });

      if (items[0] != undefined) {
        if (items[0]["customer"] !== "" && items[0]["phoneNumber"] !== "") {
          setExistingMailboxCustomer(items[0]["customer"]);
          setExistingMailboxPhoneNumber(items[0]["phoneNumber"]);
        }
        setValidMailbox(true);
      } else {
        setExistingMailboxCustomer("");
        setExistingMailboxPhoneNumber("");
        setValidMailbox(false);
      }
    });
    return () => {
      unsub();
    };
  };

  const handleAddMailbox = () => {
    try {
      updateDoc(doc(db, "users", mailboxID), {
        customer: customer,
        phoneNumber: phoneNumber,
      });
      setSubmitMailbox(true);
    } catch (err) {
      setSubmitMailbox(false);
    }
  };

  return (
    <div className="add-mailbox">
      <Text as="b" fontSize="4xl">
        Add Mailbox
      </Text>
      <div className="mailbox-info">
        <HStack spacing="20px">
          <FormControl id="mailbox-number" isRequired>
            <FormLabel>Mailbox Number</FormLabel>
            <NumberInput
              max={3000}
              min={1}
              onChange={(e) => {
                setMailboxNumber(e);
                checkEmptyMailbox(e);
                setSubmitMailbox(false);
              }}
            >
              <NumberInputField />
              <NumberInputStepper>
                <NumberIncrementStepper />
                <NumberDecrementStepper />
              </NumberInputStepper>
            </NumberInput>
          </FormControl>
          <FormControl id="customer-name" isRequired>
            <FormLabel>Customer Name</FormLabel>
            <Input
              placeholder="John Smith"
              onChange={(e) => {
                setCustomer(e.target.value);
              }}
            />
          </FormControl>
          <FormControl id="phone-number" isRequired>
            <FormLabel>Phone Number (no spaces/dashes/+#)</FormLabel>
            <Input
              placeholder="1234567890"
              onChange={(e) => {
                setPhoneNumber(e.target.value);
              }}
            />
          </FormControl>
        </HStack>
        <Text className="status-text">
          {submitMailbox
            ? "Successfully added/updated " +
              customer +
              " to mailbox #" +
              mailboxNumber +
              " with phone number " +
              phoneNumber +
              "."
            : validMailbox
            ? existingMailboxCustomer == "" && existingMailboxPhoneNumber == ""
              ? "Mailbox #" + mailboxNumber + " is available."
              : "Mailbox #" +
                mailboxNumber +
                " has existing customer " +
                existingMailboxCustomer +
                " with phone number " +
                existingMailboxPhoneNumber +
                ". Updating this mailbox will overwrite any current information of this mailbox."
            : mailboxNumber != "" &&
              "ERROR: Invalid mailbox number (mailbox does not exist)"}
        </Text>
        <Text className="submit-text"></Text>
      </div>
      <Button
        className="add-mailbox-button"
        onClick={() => handleAddMailbox()}
        isDisabled={
          phoneNumber === "" ||
          mailboxNumber === "" ||
          customer === "" ||
          validMailbox == false
        }
      >
        Add Mailbox
      </Button>
    </div>
  );
};

export default AddMailbox;
