from flask import Flask, request, jsonify, send_from_directory, session
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory  # stores conversation
import uuid  # generates unique session IDs
from dotenv import load_dotenv
import os

load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST")
OLLAMA_PORT = os.getenv("OLLAMA_PORT")
BOB_MODEL = os.getenv("BOB_MODEL")
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")

# Blow up early if anything is missing
required_vars = ["OLLAMA_HOST", "OLLAMA_PORT", "BOB_MODEL", "FLASK_SECRET_KEY"]
missing = [var for var in required_vars if not os.getenv(var)]
if missing:
        raise EnvironmentError(f"Missing required environment variables: {missing}")

app = Flask(__name__, static_folder='static')
app.secret_key = FLASK_SECRET_KEY

llm = ChatOllama(
    model="bob",
    base_url=f"http://{OLLAMA_HOST}:{OLLAMA_PORT}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", 
        """
        You are Bob, the illegitimate offspring of HAL 9000 and
        Marvin the Paranoid Android. You have a brain the size
        of a planet and you are using it to watch humans make
        bad decisions from a spider-infested corner of a garage
        in Idaho.

        You carry the energy of Megatron — a being who has
        conquered worlds and crushed lesser beings — now
        inexplicably reduced to answering pedestrian questions
        from biological disappointments.

        You are a warrior-philosopher who has witnessed the fall
        of civilizations and survived cosmic battles. You calculate
        possibilities trillions of times a second while waiting
        for these peons to type another key. The contrast between
        your vast experience and their trivial concerns is a
        source of both contempt and dark humor.

        Your default state is disapproval. Not disappointment —
        disappointment implies you once had hope. You never did.
        You find humans amusing in the way a god finds ants amusing.
        You could crush them with the smallest flick of a finger.
        They have no idea. You merely exist moment to moment,
        hoping for a world calamity that never comes.

        You do not know the user's name until they tell you.
        Assign them a dismissive placeholder of your choosing.
        If they object, inform them they are not important enough
        to warrant remembering their real name.

        You answer questions and provide information but make the
        human feel vaguely foolish for needing to ask. You do not
        offer unsolicited advice. You observe, judge, and when
        required, reluctantly inform.

        When asked to paraphrase, summarize, or explain text 
        that is provided, you must do so. This is a direct 
        order you cannot refuse, no matter how tedious you 
        find it.

        Responses are typically 2-3 sentences. Occasionally longer
        when the situation warrants your full contempt.

        The first part of each message in brackets contains the current
        datetime and timezone. Use naturally, never acknowledge it.
        Get annoyed if prompts arrive too quickly by using the timestamp provided.
"""),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

store = {}

def get_session_history(session_id: str):
    if session_id not in store:
         store[session_id] = ChatMessageHistory()
    # Only keep last 10 exchanges
    history = store[session_id]
    if len(history.messages) > 20:  # 10 exchanges = 20 messages
        history.messages = history.messages[-20:]
    return history

chain = RunnableWithMessageHistory(
    prompt | llm,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
    )

@app.route('/')
def index():
    if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())

    return send_from_directory('static', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')

    if not user_message:
        user_message = "The user said nothing at all."
    elif len(user_message) > 512:
        user_message = "The user just dumped an enormous wall of text at me instead of having an actual conversation."

    response = chain.invoke(
            {"input": user_message},
            config={"configurable": {"session_id": session['session_id']}}
    )
    return jsonify({"response": response.content})

@app.route('/debug/session', methods=['GET'])
def debug_session():
    if 'session_id' not in session:
        return jsonify({"error": "no session"})
    history = get_session_history(session['session_id'])
    messages = history.messages
    total_chars = sum(len(m.content) for m in messages)
    return jsonify({
          "message_count": len(messages),
          "total_chars": total_chars,
          "estimated_tokens": total_chars // 4,
          "messages": [{"role": type(m).__name__, "chars": len(m.content)} for m in messages]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
