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
  VStack,
  Textarea,
} from "@chakra-ui/react";
import firebase from "../../Firebase";
import { onSnapshot, collection, query, where } from "firebase/firestore";
import axios from "axios";
import "./CustomMessage.css";

const CustomMessage = () => {
  const [mailboxNumber, setMailboxNumber] = useState("");
  const [customer, setCustomer] = useState("N/A");
  const [phoneNumber, setPhoneNumber] = useState("N/A");
  const [message, setMessage] = useState("");
  const [idle, setIdle] = useState(true); // do not display any status at start
  const [messageSent, setMessageSent] = useState(false);
  const [sendMessageError, setSendMessageError] = useState(false);
  const [sentCustomer, setSentCustomer] = useState("N/A");
  const [sentPhoneNumber, setSentPhoneNumber] = useState("N/A");

  const updateCustomerInfo = (e: any) => {
    const q = query(
      collection(firebase, "users"),
      where("mailboxNumber", "==", parseInt(e, 10))
    );
    const unsub = onSnapshot(q, (querySnapshot) => {
      const items: any[] = [];
      querySnapshot.forEach((doc) => {
        items.push(doc.data());
      });

      if (items[0] == undefined) {
        setCustomer("N/A");
        setPhoneNumber("N/A");
      } else {
        if (items[0]["customer"] != "") {
          setCustomer(items[0]["customer"]);
        } else {
          setCustomer("N/A");
        }

        if (items[0]["phoneNumber"] != "") {
          setPhoneNumber(items[0]["phoneNumber"]);
        } else {
          setPhoneNumber("N/A");
        }
      }
    });
    return () => {
      unsub();
    };
  };

  const handleSendText = async () => {
    setMessageSent(false);
    setIdle(false);
    setSendMessageError(false);

    await axios
      .get(
        `/.netlify/functions/api?message=${
          "Incoming message from Mailpost Sammamish (please do not reply):%0a%0a" +
          message
        }&recipient=${phoneNumber}`
      )
      .then((response) => {
        setMessageSent(true);
        setSentCustomer(customer);
        setSentPhoneNumber(phoneNumber);
        console.log(response);
      })
      .catch((error) => {
        setSendMessageError(true);
        console.log(error);
      });
  };

  return (
    <div className="custom-message">
      <Text as="b" fontSize="4xl">
        Send a Custom Message
      </Text>
      <div className="find-customer">
        <HStack spacing="20px">
          <FormControl id="mailbox-number" isRequired>
            <FormLabel>Mailbox Number</FormLabel>
            <NumberInput
              max={3000}
              min={1}
              onChange={(e) => {
                setMailboxNumber(e);
                updateCustomerInfo(e);
              }}
              width="300px"
            >
              <NumberInputField />
              <NumberInputStepper>
                <NumberIncrementStepper />
                <NumberDecrementStepper />
              </NumberInputStepper>
            </NumberInput>
          </FormControl>
          <VStack className="customer-info" spacing="0px">
            <Text as="b">Customer: {customer}</Text>
            <Text as="b">Phone #: {phoneNumber}</Text>
            {messageSent && !sendMessageError && (
              <Text as="i" colorScheme="green" color="green.500">
                Message to {sentCustomer} at {sentPhoneNumber} sent
                successfully.
              </Text>
            )}
            {!idle && !messageSent && !sendMessageError && (
              <Text as="i" colorScheme="blue" color="blue.500">
                Sending message...
              </Text>
            )}
            {sendMessageError && !messageSent && (
              <Text as="i" colorScheme="red" color="red.500">
                ERROR sending message.
              </Text>
            )}
          </VStack>
        </HStack>
      </div>
      <div className="textarea">
        <Textarea
          placeholder="Add custom message here"
          onChange={(e) => {
            setMessage(e.target.value);
            console.log(e.target.value);
          }}
        />
      </div>
      <Button
        className="send-text-button"
        onClick={() => handleSendText()}
        isDisabled={message === "" || mailboxNumber === ""}
      >
        Send Text
      </Button>
    </div>
  );
};

export default CustomMessage;
