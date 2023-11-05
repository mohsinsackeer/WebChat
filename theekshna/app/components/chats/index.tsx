import React from "react";
import ChatWindow from "./chatwindow";
import Contacts from "./contacts";
import ChatPageStyles from "./styles/chatPageStyles";

const ChatPage: React.FC = () => {
  return (
    <ChatPageStyles>
      <Contacts />
      <ChatWindow />
    </ChatPageStyles>
  );
};
export default ChatPage;
