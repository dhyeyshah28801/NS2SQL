## A Speech To SQL With Database Specific Context Integration Using RAG and LLMs.
First of all you need to install all the modules from the `root` of this repository using the command:
    ```
        pip install -r requirements.txt
    ```
1. In your terminal, go into the `src` folder using the `cd` command.
2. Run `__init__.py` using the command (Depending on your python configurations)
    ```
        python __init__.py
                OR
        python3 __init__.py
    ```
3. Speak the instruction you want to perform on the database when you see a prompt to speak.
4. Once the recording is finished, you should see the SQL query to perform the instructions on the database displayed.

## Evaluating Tests
To check the data provided in evaluations section of the report you can use the following:
1. In your terminal, go into the `src` folder using the `cd` command.
2. Run `__test__.py` using the command (Depending on your python configurations)
    ```
        python __test__.py
                OR
        python3 __test__.py
    ```