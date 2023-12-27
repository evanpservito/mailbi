import { Button, Input, Switch, Text } from "@chakra-ui/react";
import {
  updateDoc,
  Timestamp,
  collection,
  getDocs,
  query,
  where,
} from "firebase/firestore";
import db from "../../Firebase";
import { useState } from "react";
import useScanDetection from "use-scan-detection";
import "./Collection.css";

const Collection = () => {
  const [trackingNumber, setTrackingNumber] = useState<String>("");
  const [manualMode, setManualMode] = useState(false);
  const [statusMessage, setStatusMessage] = useState("");

  useScanDetection({
    onComplete: (num) => {
      if (!manualMode) {
        // Temporary fix to "Shift" substring appearing in barcode scan mode
        setTrackingNumber(num.replace(/Shift/g, ""));
        collectPackage(num.replace(/Shift/g, ""));
      }
    },
    minLength: 4,
  });

  const collectPackage = async (num: String) => {
    const q = query(
      collection(db, "pending-packages"),
      where("trackingNumber", "==", num)
    );
    const querySnapshot = await getDocs(q);
    if (querySnapshot.empty == true) {
      setStatusMessage(
        "ERROR: tracking number " + num + " does not exist in the system."
      );
    } else {
      querySnapshot.forEach((doc) => {
        updateDoc(doc.ref, {
          status: "Collected",
          dateCollected: Timestamp.fromDate(new Date()),
        });
        setStatusMessage("Package " + num + " successfully updated.");
      });
    }
  };

  return (
    <div className="collection">
      <Text as="b" fontSize="4xl">
        Collection
      </Text>

      <div className="input-collection">
        <div className="mode">
          <Text as="b">{manualMode ? "Manual Mode" : "Scan Mode"}</Text>
          <Switch
            className="switch"
            size="lg"
            onChange={(e) => {
              setManualMode(!manualMode);
              e.currentTarget.blur();
            }}
          />
        </div>
        <Text>
          {manualMode
            ? "Manual Mode: manually enter a tracking number to mark as collected."
            : "Scan Mode: automatically detect and update any scanned package as collected."}
        </Text>
        <Text as="b">Tracking Number</Text>
        <div className="manual-collection">
          <Input
            placeholder="Barcode"
            onChange={(e) => setTrackingNumber(e.target.value)}
            isDisabled={!manualMode}
            width="500px"
          />
          <Button
            isDisabled={!manualMode}
            onClick={() => collectPackage(trackingNumber)}
          >
            Submit
          </Button>
        </div>
        <Text>{statusMessage}</Text>
      </div>
    </div>
  );
};

export default Collection;
