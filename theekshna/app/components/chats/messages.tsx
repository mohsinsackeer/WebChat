import { COLORS } from "@/app/constants/global";
import { useAppSelector } from "@/app/redux/hook";
import styled from "styled-components";
import ReciveList from "./styles/messagereciveList";
import SendList from "./messagesendList";

type Props = {
  list: string[];
};
export const MessagesStyle = styled.div`
  color: ${COLORS.GREY};
  overflow-y: scroll;
  display: flex;
  flex-direction: column;
  height: calc(100% - 100px);
`;
const Messages: React.FC<Props> = () => {
  const { selectedChat } = useAppSelector((state) => state.globalReducer);
  return (
    <MessagesStyle>
      <ReciveList />
      <SendList />
    </MessagesStyle>
  );
};

export default Messages;
