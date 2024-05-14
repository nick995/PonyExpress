import React, { useState } from "react";
import { useApi } from "../hooks";
import { useMutation, useQueryClient } from "react-query";


function MessageMenu({onClick, isEditing, message }) {
  const [isOpen, setIsOpen] = useState(false);
  const api = useApi();
  const queryClient = useQueryClient();

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  //https://stackoverflow.com/questions/62340697/react-query-how-to-usequery-when-button-is-clicked

  const removeMutation = useMutation({
    mutationFn: () =>
      api.remove(`/chats/${message.chat_id}/messages/${message.id}`),
    onSuccess: (data) => {
      console.log("message removed");
      queryClient.invalidateQueries({
        queryKey: ["chats", `${message.chat_id}`],
      });
    },
  });

  const handleDelete = () => {
    removeMutation.mutate();
  };

  const handleEdit = () => {
    onClick();
  };

  return (
    <div className="relative inline-block">
      <button
        onClick={toggleMenu}
        type="button"
        className="inline-flex items-center justify-center p-2 w-10 h-10 text-sm text-gray-500 rounded-lg hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600 z-10"
        aria-expanded={isOpen ? "true" : "false"}
        aria-label={isOpen ? "Close menu" : "Open menu"}
      >
        <span className="sr-only">{isOpen ? "Close menu" : "Open menu"}</span>
        <svg
          className="w-3 h-3"
          aria-hidden="true"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 17 14"
        >
          <path
            stroke="currentColor"
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth="2"
            d="M1 1h15M1 7h15M1 13h15"
          />
        </svg>
      </button>

      {isOpen && (
        <div className="absolute mt-2 w-20 bg-blue-300 dark:bg-gray-800 rounded-lg shadow-lg">
          <button
            className="block w-full py-2 px-3 text-gray-900 rounded-t hover:bg-blue-500 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white"
            onClick={handleEdit}
          >
            Edit
          </button>
          <button
            className="block w-full py-2 px-3 text-gray-900 rounded-b hover:bg-blue-500 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white"
            onClick={handleDelete}
          >
            Delete
          </button>
        </div>
      )}
    </div>
  );
}

export default MessageMenu;
