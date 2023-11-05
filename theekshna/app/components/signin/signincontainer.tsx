import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import { CssTextField, SignInStyle } from "./styles/SignInStyle";
import { useRouter } from "next/navigation";

const SignInContainer: React.FC = () => {
  const router = useRouter();
  const handleOnSubmit = () => {
    router.push("/chats");
  };
  return (
    <SignInStyle>
      <Box
        component="form"
        sx={{
          "& .MuiTextField-root": { width: "500px", height: "75px" },
        }}
        noValidate
        autoComplete="off"
      >
        <div className="signinform">
          <CssTextField
            className="textfld"
            id="outlined-size-small"
            label="Username"
          />
          <CssTextField
            className="textfld"
            id="outlined-size-small"
            label="Password"
          />
          <Button
            className="signinbtn"
            fullWidth
            variant="contained"
            onClick={handleOnSubmit}
          >
            SignIn
          </Button>
        </div>
      </Box>
    </SignInStyle>
  );
};

export default SignInContainer;
