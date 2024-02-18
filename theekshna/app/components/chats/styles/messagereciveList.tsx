import { COLORS } from "@/app/constants/global";
import styled from "styled-components";

export const ReciveListStyle = styled.div`
  height: 20px;
  padding: 8px;
  max-width: 500px;
  background-color: ${COLORS.BLACK};
  margin-top: 2px;
  color: white;
  margin-bottom: 2px;
  margin-left: 30px;
  align-items: flex-start;
  border-radius: 8px;
`;
const ReciveList: React.FC = () => {
  return <ReciveListStyle>message</ReciveListStyle>;
};

export default ReciveList;
