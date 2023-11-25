# Secret-Santa
A small python program that generates secret santas pairs and emails them to specified accounts

https://secret-santa.hectorbennett.com/

---

send POST request with data of the form

```json
{
  "santas": [
    {
      "santa": "human 1",
      "email": "human1@email.com"
    },
    {
      "santa": "human 2",
      "email": "human2@email.com"
    },
    {
      "santa": "human 3",
      "email": "human3@email.com"
    },
    {
      "santa": "human 4",
      "email": "human4@email.com"
    },
    {
      "santa": "human 5",
      "email": "human5@email.com"
    },
    {
      "santa": "human 6",
      "email": "human6@email.com"
    }
  ],
  "invalid_pairs": [
    [
      "human 1",
      "human 2",
      "human 4"
    ],
    [
      "human 4",
      "human 5"
    ]
  ],
  "message": "Dear {santa}, buy something for {giftee}",
  "subject": "Hi {santa}",
  "test": true
}
```


# Setup

Create a venv with

```
python3 -m venv ./venv
```

Activate with

```
source ./venv/bin/activate
```

Install dependencies with

```
pip install -r /path/to/requirements.txt
```

Create a `.env` file containing your mail deets, and then run the app with

```
flask run
```
