import { useAppDispatch } from "@/app/redux/hook";
import ListItemStyle from "./styles/listItemStyle";
import { setSelectedChat } from "@/app/redux/slices/globalSlice";
type Props = {
  name: string;
  lastmessage: string;
};

const ListItem: React.FC<Props> = ({ name, lastmessage }) => {
  const useDispatch = useAppDispatch();
  return (
    <ListItemStyle onClick={() => useDispatch(setSelectedChat(name))}>
      <img className="profile-pic" src="/images/profile.png" />
      <div className="contact">
        <div className="contact-name">{name}</div>
        <div className="last-msg">{lastmessage}</div>
      </div>
      <div className="notification-div">
        <div>1</div>
      </div>
    </ListItemStyle>
  );
};

export default ListItem;
