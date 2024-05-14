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

function NewMessageForm({chatId}){
    const queryClient = useQueryClient();
    const api = useApi()
    const [text, setText] = useState("");

    const mutation = useMutation({
        mutationFn: () => (
          api.post(
            `/chats/${chatId}/messages`,
            {
              text
            },
          ).then((response) => response.json())          
        ),
        onSuccess: (data) => {
            console.log("message sent")
          queryClient.invalidateQueries({
            queryKey: ["chats"],
          });
          // reset the text
          setText("")        
        },
      });
    
      const onSubmit = (e) => {
        e.preventDefault();
        mutation.mutate();
        
        // e.target.reset();
      };
    
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
            <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded-r-md hover:bg-blue-600 transition duration-300">Send</button>

        </form>
    );
}

function NewMessage({chatId}){
    return(
        <div>
            <NewMessageForm chatId={chatId}/>
        </div>
    );
}

export default NewMessage