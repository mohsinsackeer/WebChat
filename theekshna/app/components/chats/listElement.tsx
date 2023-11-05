import ListItemStyle from "./styles/listItemStyle";

const ListItem: React.FC = () => {
  return (
    <ListItemStyle>
      <img className="profile-pic" src="/images/profile.png" />
      <div className="contact">
        <div className="contact-name">Name</div>
        <div className="last-msg">LastMessage</div>
      </div>
      <div className="notification-div">
        <div>1</div>
      </div>
    </ListItemStyle>
  );
};

export default ListItem;
