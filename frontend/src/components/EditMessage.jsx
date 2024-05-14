import {useState} from "react";
import { useMutation, useQueryClient } from "react-query";
import { useAuth, useApi } from "../hooks";
function Input(props){
    return(
        <div className="w-full">
            <label className="text-xl text-black-400" htmlFor={props.message}>
                {props.message}
            </label>
            <input
                {...props}
                className="w-full px-3 py-2 border rounded-l-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
        </div>
    )
}

function NewMessageForm({message, onClick}){
    const queryClient = useQueryClient();
    const api = useApi()
    const [text, setText] = useState(message.text);
    console.log("new message here")
    console.log(message)

    const mutation = useMutation({
        mutationFn: () => (
          api.put(
            `/chats/${message.chat_id}/messages/${message.id}`,
            {
              text
            },
          ).then((response) => response.json())          
        ),
        onSuccess: (data) => {
            console.log("message edited")
          queryClient.invalidateQueries({
            queryKey: ["chats", `${message.chat_id}`],
          });
          // reset the text
          setText("")        
        },
      });
    
      const onSubmit = (e) => {
        e.preventDefault();
        mutation.mutate();
        onClick();
      };

      const cancle = (e) => {
        e.preventDefault();
        onClick();
      }
    
    return(
        <form className="p-4 border-t flex" onSubmit={onSubmit}>
                <Input
                    name="text"
                    type="text"
                    value={text}
                    placeholder="Type a message"
                    onChange={(e) => setText(e.target.value) }
                    id = "message"
                />
            {/* <Button type="submit">Send</Button> */}
            <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded-r-md hover:bg-blue-600 transition duration-300">Edit</button>
            <button onClick={cancle} className="bg-blue-500 text-white px-4 py-2 rounded-r-md hover:bg-blue-600 transition duration-300">Cancle</button>

        </form>
    );
}

function EditMessage({message, onClick}){
    return(
        <div>
            <NewMessageForm message={message} onClick={onClick}/>
        </div>
    );
}

export default EditMessage