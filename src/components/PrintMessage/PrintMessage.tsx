import { Text } from "@chakra-ui/react";
import Barcode from "react-barcode";
import "./PrintMessage.css";

const PrintMessage = ({ mailboxNumber, trackingNumber, packageType }: any) => {
  /* add function to get tracking number and date */
  const today = new Date();
  const currentDate =
    today.getMonth() + 1 + "/" + today.getDate() + "/" + today.getFullYear();
  return (
    <div>
      <div className="print-sheet-first">
        <Text as="b" fontSize="4xl">
          Mailpost Alert! You have a package ready for pickup.
        </Text>
        <Text fontSize="xl">Mailbox Number: {mailboxNumber} </Text>
        <Text fontSize="xl">Tracking Number: {trackingNumber}</Text>
        <Text fontSize="xl">Package Type: {packageType}</Text>
        <Text fontSize="xl">Delivery Date: {currentDate}</Text>
        <div className="signatures">
          <Text>Customer Signature: ____________________</Text>
          <Text>Staff Signature: ____________________</Text>
          <Text>Pickup Date: ____________________</Text>
        </div>
        <div className="barcode">
          <Barcode
            marginTop={40}
            fontSize={10}
            height={30}
            width={1}
            value={trackingNumber}
          />
        </div>
      </div>
      <div className="print-sheet-second">
        <Text fontSize="2xl">Mailbox Number:</Text>
        <Text as="b" fontSize="8xl">
          {mailboxNumber}
        </Text>
        <Text fontSize="xl">Tracking Number: {trackingNumber}</Text>
        <Text fontSize="xl">Package Type: {packageType}</Text>
        <Text fontSize="xl">Delivery Date: {currentDate}</Text>
      </div>
    </div>
  );
};

export default PrintMessage;
