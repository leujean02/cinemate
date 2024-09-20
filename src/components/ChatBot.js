import React, { useState } from 'react';
import './ChatBot.css';
import AWS from 'aws-sdk';

const ChatBot = () => {
  const [messages, setMessages] = useState([
    { sender: 'bot', text: "Hi, I'm CineMate! How can I assist you today?" }
  ]);
  const [userInput, setUserInput] = useState('');

  const lexRuntime = new AWS.LexRuntime({
    region: 'ap-northeast-2', 
    credentials: new AWS.CognitoIdentityCredentials({
      IdentityPoolId: 'ap-northeast-2:2a13d0de-fb0d-48b4-bb68-4f8ee5d4d4b5',  
    }),
  });

  const handleSend = () => {
    if (userInput.trim() === '') return;

    setMessages([...messages, { sender: 'user', text: userInput }]);

    const params = {
      botAlias: '$LATEST',  
      botName: 'CineMate',  
      inputText: userInput,
      userId: 'user',  
    };

    lexRuntime.postText(params, (err, data) => {
      if (err) {
        console.log(err, err.stack); 
        setMessages(prevMessages => [
          ...prevMessages,
          { sender: 'bot', text: "Sorry, I encountered an error." }
        ]);
      } else {
        setMessages(prevMessages => [
          ...prevMessages,
          { sender: 'bot', text: data.message || "I'm not sure how to respond to that." }
        ]);
      }
    });

    setUserInput('');
  };

  return (
    <div className="chatbot-container">
      <div className="chat-window">
        <div className="messages">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`message ${message.sender === 'bot' ? 'bot' : 'user'}`}
            >
              {message.text}
            </div>
          ))}
        </div>
        <div className="input-area">
          <input
            type="text"
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            placeholder="Type a message..."
          />
          <button onClick={handleSend}>Send</button>
        </div>
      </div>
    </div>
  );
};

export default ChatBot;
