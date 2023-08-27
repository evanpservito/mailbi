import React, { useRef, useState } from "react";
import TrackingEntry from "../TrackingEntry/TrackingEntry";
import PrintMessage from "../PrintMessage/PrintMessage";
import { useReactToPrint } from "react-to-print";
import { Text, Button } from "@chakra-ui/react";
import "./TrackingLog.css";

const TrackingLog = () => {
  const componentRef = useRef(null);
  const [mailboxNumber, setMailboxNumber] = useState("");
  const [trackingNumber, setTrackingNumber] = useState("");
  const [trigger, setTrigger] = useState(0);
  const [isFilled, setIsFilled] = useState(false);
  const [packageType, setPackageType] = useState("");

  const updateMailboxNumber = (newMailboxNumber: any) => {
    setMailboxNumber(newMailboxNumber);
  };

  const updateTrackingNumber = (newTrackingNumber: any) => {
    setTrackingNumber(newTrackingNumber);
  };

  const updateIsFilled = (newIsFilled: any) => {
    setIsFilled(newIsFilled);
  };

  const updatePackageType = (newPackageType: any) => {
    setPackageType(newPackageType);
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

  const handleSendText = () => {
    setTrigger((trigger) => trigger + 1);
  };

  return (
    <div>
      <Text as="b" fontSize="2xl">
        Mailpost Package Management
      </Text>
      <TrackingEntry
        updateMailboxNumber={updateMailboxNumber}
        updateTrackingNumber={updateTrackingNumber}
        updateIsFilled={updateIsFilled}
        updatePackageType={updatePackageType}
        trigger={trigger}
      />

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
    </div>
  );
};

export default TrackingLog;
