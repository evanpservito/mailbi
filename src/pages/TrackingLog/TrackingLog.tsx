import React, { useRef, useState, useEffect } from "react";

import PrintMessage from "../../components/PrintMessage/PrintMessage";
import { useReactToPrint } from "react-to-print";
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
  Button,
  VStack,
  StackDivider,
} from "@chakra-ui/react";
import firebase from "../../Firebase";
import { onSnapshot, collection, query, where } from "firebase/firestore";
import axios from "axios";
import { UserAuth } from "../../context/AuthContext";
import { Link } from "react-router-dom";
import "./TrackingLog.css";

const TrackingLog = () => {
  const componentRef = useRef(null);
  const [mailboxNumber, setMailboxNumber] = useState("");
  const [trackingNumber, setTrackingNumber] = useState("");
  const [isFilled, setIsFilled] = useState(false);
  const [packageType, setPackageType] = useState("");
  const [customer, setCustomer] = useState("N/A");
  const [phoneNumber, setPhoneNumber] = useState("N/A");
  const [sentCustomer, setSentCustomer] = useState("N/A");
  const [sentPhoneNumber, setSentPhoneNumber] = useState("N/A");
  const [idle, setIdle] = useState(true); // do not display any status at start
  const [messageSent, setMessageSent] = useState(false);

  const { user, logOut } = UserAuth();

  const handleSignOut = async () => {
    try {
      await logOut();
    } catch (error) {
      console.log(error);
    }
  };
  useEffect(() => {
    if (mailboxNumber != "" && trackingNumber != "" && packageType != "") {
      setIsFilled(true);
    } else {
      setIsFilled(false);
    }
  }),
    [mailboxNumber, trackingNumber, packageType];

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
        setSentCustomer(customer);
        setSentPhoneNumber(phoneNumber);
        console.log(response);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const Message = React.forwardRef<HTMLInputElement>((_props, ref) => {
    return (
      <div ref={ref}>
        <PrintMessage
          mailboxNumber={mailboxNumber}
          trackingNumber={trackingNumber}
          packageType={packageType}
        />
      </div>
    );
  });

  const handlePrint = useReactToPrint({
    content: () => componentRef.current,
  });

  return (
    <div>
      <div className="title">
        <Text as="b" fontSize="2xl">
          Mailbi
        </Text>
      </div>
      <Text>Welcome, {user?.displayName}</Text>
      <div className="tracking-entry">
        <div className="entry">
          <HStack
            spacing="20px"
            divider={<StackDivider borderColor="gray.200" />}
          >
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
            <VStack className="customer-info" spacing="0px">
              <Text as="b">Customer: {customer}</Text>
              <Text as="b">Phone #: {phoneNumber}</Text>
              {messageSent && (
                <Text as="i" colorScheme="green" color="green.500">
                  Message to {sentCustomer} at {sentPhoneNumber} sent
                  successfully.
                </Text>
              )}
              {!idle && !messageSent && (
                <Text as="i" colorScheme="blue" color="blue.500">
                  Sending message...
                </Text>
              )}
            </VStack>
          </HStack>
        </div>
      </div>

      <div style={{ display: "none" }}>
        <Message ref={componentRef} />
      </div>

      {isFilled && (
        <div className="submit-buttons">
          <Button className="send-text-button" onClick={() => handleSendText()}>
            Send Text
          </Button>
          <Button className="print-button" onClick={() => handlePrint()}>
            Print Notification
          </Button>
        </div>
      )}

      {user?.displayName ? (
        <Button onClick={handleSignOut}>Logout</Button>
      ) : (
        <Link to="/login">Login</Link>
      )}
    </div>
  );
};

export default TrackingLog;
