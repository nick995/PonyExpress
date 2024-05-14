import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "react-query";
import { Link, Navigate, useNavigate, useParams } from "react-router-dom";
import NewMessage from "./NewMessage";
import { useApi, useUser } from "../hooks";
import MessageMenu from "./MessageMenu";
import EditMessage from "./EditMessage";
const h3ClassName =
  "py-1 border-2 border-[#E3CAA5] rounded text-center font-bold mb-3";

function ChatContainer({ chats, chatId }) {
  const active = (chat) => chat.id === parseInt(chatId);

  return (
    <div className="flex flex-col gap-4 overflow-auto border-2 border-[#F08A5D] p-2">
      <h3 className={h3ClassName}>pony express</h3>
      {chats.map((chat) => (
        <ChatCard key={chat.id} chat={chat} active={active(chat)} />
      ))}
    </div>
  );
}

function ChatCard({ chat, active }) {
  const className = [
    "flex flex-col",
    "border-2 rounded",
    "mb-4 p-2",
    "bg-[#FFFBE9]",
    "hover:bg-[#E3CAA5]",
    active ? "bg-[#AD8B73] border-[#AD8B73] border-4" : "border-none",
  ].join(" ");

  return (
    <Link to={`/chats/${chat.id}`}>
      <div className={className}>
        <div className="chat-name"> {chat.name}</div>
        {/* <div className="chat-detail">{chat.username}</div> */}
        {/* <div className="chat-created-at">{chat.created_at} </div> */}
      </div>
    </Link>
  );
}

function MessageQuery() {
  // getting chatId
  const api = useApi();
  // const user = useUser();
  const { chatId } = useParams();
  const navigate = useNavigate();
  const { data, isLoading } = useQuery({
    queryKey: ["chats", chatId],
    queryFn: () =>
      chatId
        ? api.get(`/chats/${chatId}/messages`).then((response) => {
            if (!response.ok) {
              response.status === 404
                ? navigate("/error/404")
                : navigate("/error");
            }
            return response.json();
          })
        : undefined,
  });
  if (!chatId) {
    return <MessageContainer messages={[]} />;
  }
  if (isLoading) {
    return <MessageContainer messages={[]} />;
  }

  if (data?.messages) {
    // if data exists and has messages key
    return (
      <div className="flex flex-col col-span-2 gap-3 border border-[#F08A5D] p-2">
        <h3 className={h3ClassName}>messages</h3>
        <MessageContainer messages={data.messages} />
        <NewMessage chatId={data.messages[0].chat_id} />
      </div>
    );
  }

  return <Navigate to="/error"></Navigate>;
}

function MessageContainer({ messages }) {
  const user = useUser();

  if (messages.length == 0) {
    return (
      <div>
        <h2 className="text-center text-2xl font-bold">
          {" "}
          Please select chat!{" "}
        </h2>
      </div>
    );
  } else {
    return (
      <>
                <div className="flex flex-col gap-5 max-h-fitted h-96 items-start overflow-y-scroll max-w-fitted">
          {messages.map((message) => (
            <MessageCard key={message.id} message={message} />
          ))}
        </div>
      </>
    );
  }
}

function MessageCard({ message }) {
  const user = useUser();
  const event = new Date(message.created_at);
  const dateString = event.toDateString() + " - " + event.toLocaleTimeString();
  const [isEditing, setIsEditing] = useState(false);
  const editing = () => {
    setIsEditing(true);
  };
  const edited = () => {
    console.log("edit is done")
    setIsEditing(false);
}
  return user.username === message.user.username ? (
    isEditing ? (
      <div className="max-w-md p-4 rounded-2xl border-gray-200 bg-gray-100 ">
        <div className="text-sm text-teal font-semibold">
          {message.user.username}
        </div>

        <EditMessage message={message} onClick={edited} />

        <div className="text-right text-xs text-grey-dark mt-1">
          {dateString}
        </div>

        <div>
          <MessageMenu
            onClick={editing}
            isEditing={isEditing}
            message={message}
          />
        </div>
      </div>
    ) : (
      <div className="flex flex-col max-w-md p-4 rounded-2xl border-gray-200 bg-gray-100 ">
      <div className="flex flex-row justify-between items-center p-0">
      <div className="text-sm text-teal font-semibold">
          {message.user.username}
        </div>
        <div>
          <MessageMenu
            onClick={editing}
            isEditing={isEditing}
            message={message}
            className="origin-top-right absolute z-50"
          />
        </div>
      </div>
        <div className="text-base mt-1 whitespace-normal overflow-x-auto">{message.text}</div>
        <div className="text-right text-xs text-grey-dark mt-1">{dateString}</div>

      </div>
    )
  ) : (
    <div className="max-w-md p-4 rounded-2xl border-gray-200 bg-gray-100">
    <div className="text-sm text-teal font-semibold">
        {message.user.username}
      </div>
        <div className="text-base mt-1 whitespace-normal overflow-x-auto">{message.text}</div>

      <div className="text-right text-xs text-grey-dark mt-1">{dateString}</div>
    </div>
  );
}

function ChatsPage() {
  const api = useApi();
  const { chatId } = useParams();
  const navigate = useNavigate();
  const { data, isLoading, error } = useQuery({
    queryKey: ["chats"],
    queryFn: () =>
      api.get(`/chats`).then((response) => {
        if (!response.ok) {
          response.status == 404 ? navigate("/error/404") : navigate("/error");
        }
        return response.json();
      }),
  });
  if (error) {
    return <Navigate to="/error" />;
  }

  if (data?.chats) {
    return (
      <div className="grid grid-cols-3 gap-5 max-h-fitted overflow-auto">
        {!isLoading && data?.chats ? (
          <ChatContainer chats={data.chats} chatId={chatId} />
        ) : (
          <></>
        )}
        <MessageQuery />
      </div>
    );
  }
}

export default ChatsPage;
