import { COLORS } from "@/app/constants/global";
import SendIcon from "@mui/icons-material/Send";
import { IconButton, InputBase } from "@mui/material";

import styled from "styled-components";

export const MessageInputStyle = styled.div`
  display: flex;
  border: 1px solid ${COLORS.GREY};
  border-radius: 10px;
  width: 896px;
  max-height: 40px;
  position: absolute;
`;

const MessageInputDiv: React.FC = () => {
  return (
    <MessageInputStyle>
      <InputBase
        multiline={true}
        sx={{ ml: 1, flex: 1, overflowY: "scroll", overflowX: "hidden" }}
        placeholder="Message"
        inputProps={{ "aria-label": "Message" }}
      />
      <IconButton type="button" sx={{ p: "10px" }} aria-label="send">
        <SendIcon />
      </IconButton>
    </MessageInputStyle>
  );
};

export default MessageInputDiv;
