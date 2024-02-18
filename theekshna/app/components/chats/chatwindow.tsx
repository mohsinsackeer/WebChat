import ChatHeader from "./chatHeader";
import MessageInputDiv from "./messageInput";
import Messages from "./messages";
import ChatWindowStyles from "./styles/ChatWindowStyle";

const ChatWindow: React.FC = () => {
  return (
    <ChatWindowStyles>
      <ChatHeader />
      <Messages list={[]} />
      <MessageInputDiv />
    </ChatWindowStyles>
  );
};

export default ChatWindow;
