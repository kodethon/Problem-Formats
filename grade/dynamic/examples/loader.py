import argparse
import imp
import json
import logging

from kutils import KQuestionBase


def get_source_path(question_name):
    return 'grader.py'


def get_metadata():
    metadata_path = '../metadata.json'
    with open(metadata_path) as f:
        return json.load(f)


def get_submission():
    submission_path = '../submission/submission.txt'
    with open(submission_path) as f:
        return f.read()


def post_question(question_cls):
    logging.info('Creating randomized question.')
    logging.info('Using subclass {}'.format(question_cls.__name__))
    question = question_cls.generate_question()
    logging.info('Question generated: {}'.format(question.data))
    print question.output_json


def grade_question(question_cls):
    logging.info('Grading submission.')
    metadata = get_metadata()
    submission = get_submission()
    logging.info('Grading submission: {}'.format(submission))
    question = question_cls.from_metadata(metadata)
    logging.info('Question recreated: {}'.format(question.data))
    print question.output_submission(submission)
    

def main():
    logging.basicConfig(level=logging.ERROR)
    
    import os
    logging.debug('Working in {}.'.format(os.getcwd()))
    
    modules = dict()
    modules['post'] = post_question
    modules['grade'] = grade_question

    parser = argparse.ArgumentParser(description = 'Kodethon loader.')
    parser.add_argument('command')
    parser.add_argument('question')
    parser.add_argument('metadata', nargs='?')
    args = parser.parse_args()
    
    source_path = get_source_path(args.question)
    logging.info('Loading specific module from {}'.format(source_path))
    imp.load_source('_', source_path)

    func = modules[args.command]
    subclass = KQuestionBase.get_subclass_by_name(args.question)
    return func(subclass)


if __name__ == '__main__':
    main()
