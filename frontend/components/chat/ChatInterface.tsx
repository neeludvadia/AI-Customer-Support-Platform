"use client";

import React, { useEffect, useState, useRef } from "react";
import { chatService } from "@/services/chat.service";
import { ConversationResponse, MessageResponse } from "@/types/chat";

export function ChatInterface() {
  const [conversations, setConversations] = useState<ConversationResponse[]>([]);
  const [activeConversationId, setActiveConversationId] = useState<number | null>(null);
  const [messages, setMessages] = useState<MessageResponse[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Load history on mount
  useEffect(() => {
    loadHistory();
  }, []);

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const loadHistory = async () => {
    try {
      const history = await chatService.getHistory();
      setConversations(history);
    } catch (error) {
      console.error(error);
    }
  };

  const loadConversation = async (id: number) => {
    setActiveConversationId(id);
    try {
      const detail = await chatService.getConversationDetail(id);
      setMessages(detail.messages);
    } catch (error) {
      console.error(error);
    }
  };

  const startNewChat = async () => {
    const title = window.prompt("Enter a name for the new chat:") || "New Chat";
    try {
      const newConv = await chatService.createConversation(title);
      setConversations([newConv, ...conversations]);
      setActiveConversationId(newConv.id);
      setMessages([]);
    } catch (error) {
      console.error(error);
    }
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    let currentConvId = activeConversationId;

    // Create a new conversation if none is active
    if (!currentConvId) {
      try {
        const newConv = await chatService.createConversation(input.substring(0, 30) + "...");
        setConversations([newConv, ...conversations]);
        setActiveConversationId(newConv.id);
        currentConvId = newConv.id;
      } catch (error) {
        alert("Failed to create conversation");
        return;
      }
    }

    // Optimistically add user message
    const userMessage = input;
    setInput("");
    const tempUserMsg: MessageResponse = {
      id: Date.now(),
      conversation_id: currentConvId!,
      sender: "user",
      content: userMessage,
      citations: [],
      ticket_id: null,
      created_at: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, tempUserMsg]);
    setIsLoading(true);

    try {
      const aiResponse = await chatService.sendMessage(currentConvId!, userMessage);
      setMessages((prev) => [...prev, aiResponse]);
    } catch (error: any) {
      alert(error.message || "Error sending message");
      // Remove optimistic message on error if desired, keeping it simple here.
    } finally {
      setIsLoading(false);
    }
  };

  const handleEscalate = async (msgIndex: number) => {
    if (!activeConversationId || isLoading) return;
    setIsLoading(true);
    try {
      const newMsg = await chatService.escalate(activeConversationId);
      setMessages((prev) => {
        const updated = [...prev];
        if (updated[msgIndex]) {
          updated[msgIndex] = { ...updated[msgIndex], ticket_id: newMsg.ticket_id };
        }
        return [...updated, newMsg];
      });
    } catch (error: any) {
      alert(error.message || "Failed to escalate");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-[calc(100vh-8rem)] bg-white rounded-xl shadow overflow-hidden border border-gray-200">
      
      {/* Sidebar for History */}
      <div className="w-1/4 border-r border-gray-200 bg-gray-50 flex flex-col">
        <div className="p-4 border-b border-gray-200">
          <button
            onClick={startNewChat}
            className="w-full flex items-center justify-center rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white shadow hover:bg-indigo-500 transition-colors"
          >
            + New Chat
          </button>
        </div>
        <div className="flex-1 overflow-y-auto p-2 space-y-1">
          {conversations.map((conv) => (
            <button
              key={conv.id}
              onClick={() => loadConversation(conv.id)}
              className={`w-full text-left px-3 py-3 rounded-lg text-sm transition-colors truncate ${
                activeConversationId === conv.id
                  ? "bg-indigo-100 text-indigo-700 font-medium"
                  : "text-gray-700 hover:bg-gray-200"
              }`}
            >
              {conv.title || "New Chat"}
            </button>
          ))}
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6 bg-white">
          {messages.length === 0 ? (
            <div className="h-full flex items-center justify-center text-gray-500 flex-col space-y-4">
              <svg className="w-12 h-12 text-indigo-200" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" /></svg>
              <p>How can I help you today?</p>
            </div>
          ) : (
            messages.map((msg, index) => (
              <div
                key={msg.id || index}
                className={`flex ${msg.sender === "user" ? "justify-end" : "justify-start"}`}
              >
                <div
                  className={`max-w-[75%] rounded-2xl px-5 py-3 text-sm ${
                    msg.sender === "user"
                      ? "bg-indigo-600 text-white shadow-md"
                      : "bg-gray-100 text-gray-800 shadow-sm"
                  }`}
                >
                  <p className="whitespace-pre-wrap leading-relaxed">{msg.content}</p>
                  
                  {/* Citations if AI */}
                  {msg.citations && msg.citations.length > 0 && (
                    <div className="mt-3 pt-3 border-t border-gray-300">
                      <p className="text-xs font-semibold mb-1 text-gray-500">Sources:</p>
                      <ul className="text-xs space-y-1">
                        {msg.citations.map((c, i) => (
                          <li key={i} className="text-indigo-600">
                            • {c.filename} (Page {c.page})
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Ticket Link if Escelated */}
                  {msg.ticket_id && (
                    <div className="mt-3 pt-3 border-t border-gray-300">
                      <span className="inline-flex items-center rounded-md bg-yellow-100 px-2 py-1 text-xs font-medium text-yellow-800">
                        Ticket Created: #{msg.ticket_id}
                      </span>
                    </div>
                  )}

                  {/* Escalate Prompt Button */}
                  {msg.sender === "assistant" && (!msg.citations || msg.citations.length === 0) && !msg.ticket_id && (
                    <div className="mt-3 pt-3 border-t border-gray-300">
                      <button
                        onClick={() => handleEscalate(index)}
                        disabled={isLoading}
                        className="inline-flex items-center rounded-md bg-white border border-gray-300 px-3 py-1.5 text-xs font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50 transition-colors"
                      >
                        Create Support Ticket
                      </button>
                    </div>
                  )}
                </div>
              </div>
            ))
          )}
          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-gray-100 rounded-2xl px-5 py-4 flex space-x-2">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200"></div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="p-4 bg-white border-t border-gray-200">
          <form onSubmit={handleSendMessage} className="flex space-x-3">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask a question..."
              className="flex-1 rounded-full border border-gray-300 px-6 py-3 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-shadow shadow-sm"
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={!input.trim() || isLoading}
              className="inline-flex items-center justify-center rounded-full bg-indigo-600 px-6 py-3 font-medium text-white transition-colors hover:bg-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed shadow-md"
            >
              Send
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
