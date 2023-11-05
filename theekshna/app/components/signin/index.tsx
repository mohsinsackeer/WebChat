import SignInContainer from "./signincontainer";
import SignInIndexStyle from "./styles/SignInIndexStyle";

const SignIn: React.FC = () => {
  return (
    <SignInIndexStyle>
      <img src="/images/loginimage.svg" />
      <SignInContainer />
    </SignInIndexStyle>
  );
};

export default SignIn;
