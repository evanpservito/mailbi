import { useState, useEffect } from "react";
import {
  Text,
  Input,
  HStack,
  FormControl,
  FormLabel,
  NumberInput,
  NumberInputField,
  NumberInputStepper,
  NumberIncrementStepper,
  NumberDecrementStepper,
} from "@chakra-ui/react";
import firebase from "../../Firebase";
import { onSnapshot, collection, query, where } from "firebase/firestore";
import axios from "axios";
import "./TrackingEntry.css";

const TrackingEntry = ({
  updateMailboxNumber,
  updateTrackingNumber,
  updateIsFilled,
  updatePackageType,
  trigger,
}: any) => {
  const [trackingNumber, setTrackingNumber] = useState("");
  const [mailboxNumber, setMailboxNumber] = useState("");
  const [customer, setCustomer] = useState("N/A");
  const [phoneNumber, setPhoneNumber] = useState("N/A");
  const [currentTrigger, setCurrentTrigger] = useState(trigger);
  const [packageType, setPackageType] = useState("");
  const [idle, setIdle] = useState(true);
  const [messageSent, setMessageSent] = useState(false);

  useEffect(() => {
    if (trigger != currentTrigger) {
      handleSendText();
      setCurrentTrigger(trigger);
    }
  }),
    [trigger];

  useEffect(() => {
    updateMailboxNumber(mailboxNumber);
    updateTrackingNumber(trackingNumber);
    updatePackageType(packageType);

    // Change Later
    if (mailboxNumber != "" && trackingNumber != "" && packageType != "") {
      updateIsFilled(true);
    } else {
      updateIsFilled(false);
    }
  }),
    [customer, mailboxNumber, trackingNumber, packageType];

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
    const message =
      "Greetings, " +
      customer +
      "! You have a package ready for pickup at Mailpost Sammamish. Tracking Number: " +
      trackingNumber;

    await axios
      .get(`/api?message=${message}&recipient=${phoneNumber}`)
      .then((response) => {
        setMessageSent(true);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  return (
    <div className="tracking-entry">
      <div className="entry">
        <HStack spacing="30px">
          <FormControl id="tracking-number" isRequired>
            <FormLabel>Tracking Number</FormLabel>
            <Input
              placeholder="0000 0000 0000 0000 00"
              onChange={(e) => {
                setTrackingNumber(e.target.value);
              }}
            />
          </FormControl>
          <FormControl id="mailbox-number" isRequired>
            <FormLabel>Mailbox Number</FormLabel>
            <NumberInput
              max={3000}
              min={1}
              onChange={(e) => {
                setMailboxNumber(e);
                updateCustomerInfo(e);
              }}
            >
              <NumberInputField />
              <NumberInputStepper>
                <NumberIncrementStepper />
                <NumberDecrementStepper />
              </NumberInputStepper>
            </NumberInput>
          </FormControl>
          <FormControl id="package-type" isRequired>
            <FormLabel>Package Type</FormLabel>
            <Input
              placeholder="A"
              onChange={(e) => {
                setPackageType(e.target.value);
              }}
            />
          </FormControl>
        </HStack>
      </div>
      <div className="info">
        <Text as="b">Customer: {customer}</Text>
        <Text as="b">Phone #: {phoneNumber}</Text>
        {messageSent && (
          <Text as="i" colorScheme="green" color="green.500">
            Message to {customer} at {phoneNumber} sent successfully.
          </Text>
        )}
        {!idle && !messageSent && (
          <Text as="i" colorScheme="blue" color="blue.500">
            Sending message...
          </Text>
        )}
      </div>
    </div>
  );
};

export default TrackingEntry;
