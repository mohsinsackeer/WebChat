import VideoCallIcon from "@mui/icons-material/VideoCall";
import ChatHeaderStyle from "./styles/chatheaderStyle";
import { useAppSelector } from "@/app/redux/hook";

const ChatHeader: React.FC = () => {
  const { selectedChat } = useAppSelector((state) => state.globalReducer);
  return (
    <ChatHeaderStyle>
      <div>{selectedChat}</div>
      <VideoCallIcon />
    </ChatHeaderStyle>
  );
};

export default ChatHeader;
