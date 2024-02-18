import { COLORS } from "@/app/constants/global";
import styled from "styled-components";

export const SendListStyle = styled.div`
  height: 20px;
  padding: 8px;
  max-width: 500px;
  background-color: ${COLORS.RED};
  margin-top: 2px;
  margin-bottom: 2px;
  color: white;
  margin-right: 30px;
  align-self: flex-end;
  border-radius: 8px;
`;
const SendList: React.FC = () => {
  return <SendListStyle>message</SendListStyle>;
};

export default SendList;
