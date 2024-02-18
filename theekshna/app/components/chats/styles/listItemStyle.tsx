import { COLORS } from "@/app/constants/global";
import styled from "styled-components";

const ListItemStyle = styled.div`
  width: 100%;
  height: 72px;
  display: flex;
  justify-content: space-around;
  align-items: center;
  border-bottom: solid 1px ${COLORS.BORDER};
  &:hover {
    background-color: ${COLORS.HOVER};
  }
  .profile-pic {
    width: 50px;
    height: 50px;
    border-radius: 100%;
  }
  .contact {
    width: calc(100% - 150px);
    font-size: 17px;
    display: flex;
    flex-direction: column;
    justify-content: space-around;
  }
  .notification-div {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-around;
    height: 20px;
    width: 20px;
    font-size: 12px;
    border-radius: 100%;
    background-color: ${COLORS.RED};
    color: white;
  }
  .last-msg {
    color: ${COLORS.LIGHT_GREY};
  }
`;
export default ListItemStyle;
