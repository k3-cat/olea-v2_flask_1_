from typing import Dict


def build_message(subject: str, to: str, template: str,
                  values: Dict[str, str]):
    data = {f'v:{k}': v for k, v in values.items()}

    data['to'] = to
    data['subject'] = subject
    data['template'] = template

    return data
