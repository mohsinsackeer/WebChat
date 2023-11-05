import { COLORS } from "@/app/constants/global";
import TextField from "@mui/material/TextField";
import styled from "styled-components";

export const SignInStyle = styled.div`
  width: 500px;
  display: flex;
  align-items: center;
  border: black 1px;
  .signinform {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
  }
  .signinbtn {
    background-color: ${COLORS.RED};
  }
  .textfld {
    border: black;
  }
`;

export const CssTextField = styled(TextField)({
  "& label.Mui-focused": {
    color: COLORS.RED,
  },
  "& .MuiInput-underline:after": {
    borderBottomColor: "#B2BAC2",
  },
  "& .MuiOutlinedInput-root": {
    "&fieldset": {
      borderColor: "#E0E3E7",
    },
    "&:hover fieldset": {
      borderColor: "#B2BAC2",
    },
    "&.Mui-focused fieldset": {
      borderColor: COLORS.RED,
    },
  },
});
