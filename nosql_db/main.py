from multiprocessing import Process

import consumer_sms
import consumer_email

BLUE = "\033[94m"
RESET = "\033[0m"

if __name__ == "__main__":
    send_email = Process(target=consumer_email.main)
    send_sms = Process(target=consumer_sms.main)

    send_email.start()
    send_sms.start()
    print(f"{BLUE}Start consuming")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print(f'{BLUE}Kill comsumers{RESET}')
    finally:
        send_sms.terminate()
        send_email.terminate()
        