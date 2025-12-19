from huggingface_hub import InferenceClient

BREAK = 15
STEP = 45


def print_real_time(total_time: int) -> float:
    real_time = int(input('Enter time spent studying: '))
    total_real_time = round(real_time * 100 / total_time, 2) if total_time != 0 else 0
    print(total_real_time, 'time')
    if total_real_time >= 100:
        total_real_time = '100.00'
    print(f'You have completed {total_real_time}% of your planned study time.')
    return total_real_time


def print_study_plan(sub: dict) -> float:
    print('Your study plan:')
    total_time = 0

    for s in sub.keys():
        time = sub.get(s)
        print(f'{s}: {time} minutes')
        total_time += time

    time_with_breaks = total_time + (total_time // STEP * BREAK)

    print(f'Total study time: {total_time} minutes')
    print(f'Total time including breaks: {time_with_breaks} minutes')
    return print_real_time(total_time)


if __name__ == '__main__':
    subjects = {}

    while True:
        subject = input('Enter subject name: ')
        if subject == '':
            break

        time = None
        while True:
            time = input(f'Enter time allocated for {subject}: ')
            if time.isnumeric():
               break

        subjects[subject] = int(time)

    if len(subjects):
        completeness = print_study_plan(subjects)

        with open('.env', 'r') as fp:
            Hug_api_key = fp.read().strip()

        client = InferenceClient(
            token=Hug_api_key,
        )
        prompt = (f"I have to prepare for my {subjects} exams. "
                  f"I've completed {completeness}% of my curriculum. My motivation should be:")

        response = client.chat.completions.create(
            model="Qwen/Qwen3-Coder-480B-A35B-Instruct",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        print(response)

