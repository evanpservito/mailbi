import { Text } from "@chakra-ui/react";
import "./PrintMessage.css";

const PrintMessage = ({ mailboxNumber, trackingNumber, packageType }: any) => {
  /* add function to get tracking number and date */
  const today = new Date();
  const currentDate =
    today.getMonth() + 1 + "/" + today.getDate() + "/" + today.getFullYear();
  return (
    <div>
      <div className="print-sheet">
        <Text as="b" fontSize="4xl">
          Mailpost Alert! You have a package ready for pickup.
        </Text>
        <Text fontSize="2xl">Mailbox Number: {mailboxNumber} </Text>
        <Text fontSize="2xl">Tracking Number: {trackingNumber}</Text>
        <Text fontSize="2xl">Package Type: {packageType}</Text>
        <Text fontSize="2xl">Delivery Date: {currentDate}</Text>
      </div>
      <div className="print-sheet-2">
        <Text fontSize="2xl">Mailbox Number:</Text>
        <Text as="b" fontSize="8xl">
          {mailboxNumber}
        </Text>
        <Text fontSize="3xl">Package Type: {packageType}</Text>
        <Text fontSize="3xl">Delivery Date: {currentDate}</Text>
      </div>
    </div>
  );
};

export default PrintMessage;
