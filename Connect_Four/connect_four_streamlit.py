import streamlit as st
import numpy as np
from langchain.llms import OpenAI

# Initialize LLM
llm = OpenAI(api_key="YOUR_API_KEY")

class ConnectFour:
    def __init__(self):
        self.board = np.zeros((6, 7))

    def drop_piece(self, column, piece):
        row = self.get_next_open_row(column)
        self.board[row, column] = piece

    def get_next_open_row(self, column):
        for row in range(5, -1, -1):
            if self.board[row, column] == 0:
                return row

    def winning_move(self, piece):
        # Check horizontal locations for win
        for c in range(7-3):
            for r in range(6):
                if self.board[r, c] == piece and self.board[r, c+1] == piece and self.board[r, c+2] == piece and self.board[r, c+3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(7):
            for r in range(6-3):
                if self.board[r, c] == piece and self.board[r+1, c] == piece and self.board[r+2, c] == piece and self.board[r+3, c] == piece:
                    return True

def generate_response(question):
    response = llm(question)
    return response

st.title("Connect Four")
game = ConnectFour()

column = st.number_input("Enter column", min_value=0, max_value=6)

if st.button("Drop piece"):
    try:
        game.drop_piece(column, 1)
        st.write(game.board)

        if game.winning_move(1):
            st.write("Player 1 wins!")
        else:
            response = generate_response(f"What's the best move in Connect Four given the current board state: {game.board}?")
            st.write(response)
    except Exception as e:
        st.write("An error occurred:", str(e))