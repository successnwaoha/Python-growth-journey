from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Field, Session, SQLModel, create_engine, select

# 1. Define the Data Model (The Table)
class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    amount: float
    category: str
    description: str
    is_expense: bool = True  # True for expense, False for income

# 2. Database Setup (SQLite)
# "finance.db" is a file that will appear in your folder
sqlite_url = "sqlite:///./finance.db"
engine = create_engine(sqlite_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI()

# This runs when the server starts
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# 3. Helper: This manages the "Session" (opening/closing the DB door)
def get_session():
    with Session(engine) as session:
        yield session

# 4. The Endpoints (CRUD)

@app.post("/transactions/", response_model=Transaction)
def create_transaction(transaction: Transaction, session: Session = Depends(get_session)):
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction

@app.get("/transactions/", response_model=List[Transaction])
def read_transactions(
    category: Optional[str] = None, # Add this optional parameter
    session: Session = Depends(get_session)
):
    # 1. Start a base query
    statement = select(Transaction)
    
    # 2. If the user provided a category, filter the results
    if category:
        statement = statement.where(Transaction.category == category)
    
    # 3. Execute the query
    transactions = session.exec(statement).all()
    return transactions

@app.get("/balance/")
def get_balance(session: Session = Depends(get_session)):
    transactions = session.exec(select(Transaction)).all()
    total = sum(t.amount if not t.is_expense else -t.amount for t in transactions)
    return {"total_balance": total}

@app.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int, session: Session = Depends(get_session)):
    transaction = session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    session.delete(transaction)
    session.commit()
    return {"ok": True}

@app.get("/expenses/")
def get_expenses(session: Session = Depends(get_session)):
    expenses = session.exec(select(Transaction).where(Transaction.is_expense == True)).all()
    total_expenses = sum(t.amount for t in expenses)
    return {"total_expenses": total_expenses, "expenses": expenses}