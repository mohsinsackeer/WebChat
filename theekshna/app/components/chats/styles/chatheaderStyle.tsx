import { COLORS } from "@/app/constants/global";
import styled from "styled-components";

const ChatHeaderStyle = styled.div`
  font-size: 20;
  height: 40px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  color: white;
  background-color: ${COLORS.RED};
`;
export default ChatHeaderStyle;
