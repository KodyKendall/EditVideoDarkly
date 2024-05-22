import { useState } from "react";
import { useMutation, useQueryClient } from "react-query";
import { useNavigate } from "react-router-dom";
import { useApi, useAuth } from "../hooks";
import Button from "./Button";

function Input(props) {
  return (
    <div className="flex flex-col py-2">
      <label className="text-s text-gray-400" htmlFor={props.name}>
        {props.name}
      </label>
      <input
        {...props}
        className="border rounded bg-transparent px-2 py-1"
      />
    </div>
  );
}

// function Checkbox(props) {
//   return (
//     <div className="flex flex-row py-2">
//       <input
//         {...props}
//         className="border rounded bg-transparent px-2 py-1"
//         type="checkbox"
//       />
//       <label className="text-s text-gray-400 ml-4" htmlFor={props.name}>
//         {props.name}
//       </label>
//     </div>
//   );
// }

function NewMessageForm({ chat_id }) {
  const queryClient = useQueryClient();
  const navigate = useNavigate();
  const { token } = useAuth();
  const api = useApi();

  const [text, setText] = useState("");

  const mutation = useMutation({
    mutationFn: () => (
      api.post(
        `/chats/${chat_id}/messages`,
        {
          text,
        },
      ).then((response) => response.json())
    ),
    onSuccess: (data) => {//scroll to bottom of chat
      queryClient.invalidateQueries({
        queryKey: ["messages", chat_id],
      });
      navigate(`/chats/${data.message.chat_id}`);
      // alternatively, we could "reset" the form
    },
  });

  const onSubmit = (e) => {
    e.preventDefault();
    mutation.mutate();
  };

  return (
    <form onSubmit={onSubmit}>
    <div className="flex flex-row justify-between">
        <Input
            type="text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            className="items-center"
            placeholder="New Message"
        />
        <Button type="submit">send</Button>
    </div>
    </form>
  );
}

function NewMessage( {chat_id} ) {
  return (
    <div className="w-96">
      <NewMessageForm chat_id={chat_id} />
    </div>
  );
}

export default NewMessage;