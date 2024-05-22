import { useQuery } from "react-query";
import { Link, Navigate, useNavigate, useParams } from "react-router-dom";
import React, { useState } from 'react';
import NewMessage from "./NewMessage";
import ScrollContainer from "./ScrollContainer";
import { useApi } from "../hooks";

//import "./ChatsPage.css";

const h3ClassName = "py-1 border-2 mb-4 border-violet-300 rounded text-center font-bold my-2"

function ChatPreview({ chat, isSelected, onSelect }) {
  const className = [
    "flex flex-col",
    "border-2 rounded border-violet-300",
    "mb-4 p-2",
    isSelected ? "bg-slate-400" : "",
    "hover:bg-slate-400",
  ].join(" ");
  return (
    <Link className={className} to={`/chats/${chat.id}`} onClick={onSelect}>
      <div className="font-extrabold">{chat.name}</div>
      {/* <div className="chat-user-ids">{(chat.user_ids || []).join(', ')}</div> */}
      <div className="text-xxs ml-2">{new Date(chat.created_at).toDateString()} - {new Date(chat.created_at).toLocaleTimeString()}</div>
    </Link>
  );
}

function ChatCardWrapper() {
    const { chatId } = useParams();
    const navigate = useNavigate();
    const api = useApi();
    const { data, isLoading } = useQuery({
      queryKey: ["messages", chatId],
      queryFn: () => (
        api.get(`/chats/${chatId}/messages`)
          .then((response) => {
            if (!response.ok) {
              throw new Error('Failed to fetch messages');
            }
            return response.json()
          })
      ),
      enabled: !!chatId, // Only run the query if chatId is present
      refetchOnWindowFocus: false, // Optional: Disable refetching on window focus if desired
    });
    
  
    if (!chatId) {
      return <ChatCard messages={{}} />;
    }
  
    if (isLoading) {
      return <div>Loading messages...</div>;
    }
  
    if (data?.messages) {
      return <ChatCard messages={data.messages} />;
    }
  
    return <Navigate to="/error" />;
  }
  
function ChatCard({ messages }) {
    // Check if messages is an empty object
    const isMessagesEmpty = Object.keys(messages).length === 0;

    if(isMessagesEmpty){
        return (
            <div className="chat-card">
                <div className="chat-card-title">
                    <h3 className="text-center font-bold my-10">Select a Chat</h3>
                </div>
            </div>
          );
    }
    else{
    return (
      <ScrollContainer>
        <div className="border-2 border-violet-300 rounded px-2 overflow-y-scroll">
          {!isMessagesEmpty &&
            messages.map((message, index) => (
              <div key={index} className="border border-violet-600 rounded my-4 px-4 py-2">
                <div className="flex flex-row justify-between">
                  <div className="font-bold text-small text-blue-500">{message.user.username}</div>
                  <div className="text-xxs">{new Date(message.created_at).toDateString()} - {new Date(message.created_at).toLocaleTimeString()}</div>
                </div>
                <div className="ml-2">{message.text}</div>
              </div>
            ))}
        </div>
      </ScrollContainer>
    );
        }
  }
  
function EmptyChatList() {
    return (
        <ChatList
          chats={[0, 1, 2, 3, 4].map((_, index) => ({
            id: `empty-${index}`,
            name: "loading...",
            user_ids: [],
            created_at: new Date().toISOString(),
          }))}
        />
      );
}

//first column taht shows chats to choose from
function ChatList({ chats, selectedChatId, setSelectedChatId }) {
  return (
    <div className="col-span flex flex-col max-h-fitted overflow-y-scroll">
      {chats.map((chat) => (
        <ChatPreview key={chat.id} chat={chat} isSelected={chat.id === selectedChatId} onSelect={() => setSelectedChatId(chat.id)} />
      ))}
    </div>
  );
}

function ChatsPage() {
  const navigate = useNavigate();
  const api = useApi();
  const { data, isLoading, error } = useQuery({
    queryKey: ["chats"],
    queryFn: () => (
      api.get("/chats")
        .then((response) => {
          if (!response.ok) {
            response.status === 404 ?
              navigate("/error/404") :
              navigate("/error");
          }
          return response.json()
        })
    ),
  });

  const [selectedChatId, setSelectedChatId] = useState(null);

  if (error) {
    return <Navigate to="/error" />
  }

  return (
    <>
      <div className="grid grid-cols-3 gap-5">
        <div className="flex flex-col">
          <h3 className={h3ClassName}>Chats</h3>
          {!isLoading && data?.chats ? (
            <ChatList chats={data.chats} selectedChatId={selectedChatId} setSelectedChatId={setSelectedChatId} />
          ) : (
            <EmptyChatList />
          )}
        </div>
        <div className="col-span-2 flex flex-col max-h-fitted">
          <h3 className={h3ClassName}>Messages</h3>
          <ChatCardWrapper />
          {selectedChatId && (
            <NewMessage chat_id={selectedChatId} />
          )}
        </div>
      </div>
    </>
  );
}

export default ChatsPage;