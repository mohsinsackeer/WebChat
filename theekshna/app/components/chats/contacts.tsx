import { useAppDispatch } from "@/app/redux/hook";
import ListItem from "./listElement";
import ContactList from "./styles/ContactList";
const Contacts: React.FC = () => {
  return (
    <ContactList>
      <ListItem name={"ADWAITH"} lastmessage={"HI"} />
      <ListItem name="Mohsin" lastmessage={"Hello"} />
    </ContactList>
  );
};

export default Contacts;
