import { useEffect, useState } from "react";
import { useAuth } from "../context/auth";
import { useUser } from "../context/user";
import Button from "./Button";
import FormInput from "./FormInput";

function Profile() {
  const { logout } = useAuth();
  const user = useUser();
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [memberinfo, setMemberinfo ] = useState("");

  const [readOnly, setReadOnly] = useState(true);

  const reset = () => {
    if (user) {
        const dateObject = new Date(user.created_at).toDateString();

      setUsername(user.username);
      setEmail(user.email);
      setMemberinfo(dateObject)
    }
  }

  useEffect(reset, [user]);

  const onSubmit = (e) => {
    e.preventDefault();
    setReadOnly(true);
  }

  const onClick = () => {
    setReadOnly(!readOnly);
    reset();
  };

  return (
    <div className="max-w-96 mx-auto px-4 py-8">
      <h2 className="text-2xl font-bold py-2">
        User information
      </h2>
      <form className="border rounded px-4 py-2 bg-white" onSubmit={onSubmit}>
        <FormInput
          name="username"
          type="text"
          value={username}
          readOnly={readOnly}
          setter={setUsername}
        />
        <FormInput
          name="email"
          type="email"
          value={email}
          readOnly={readOnly}
          setter={setEmail}
        />

        <FormInput
          name="member since:"
          type="memberInfo"
          value={memberinfo}
          readOnly={readOnly}
          setter={setMemberinfo}
        />
        {!readOnly &&
          <Button className="mr-8" type="submit">
            update
          </Button>
        }

      </form>
      <Button onClick={logout}>
        logout
      </Button>
    </div>
  );
}

export default Profile;
