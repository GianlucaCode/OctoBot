import logging

from config.cst import START_PENDING_EVAL_NOTE
from tools.evaluators_util import check_valid_eval_note


class EvaluatorDivergenceAnalyser:
    def __init__(self):
        self.average_note = None
        self.average_counter = None
        self.matrix = None

        self.DIVERGENCE_THRESHOLD = 0.25

        self.logger = logging.getLogger(self.__class__.__name__)

    def update(self, matrix):
        self.average_note = 0
        self.average_counter = 0
        self.matrix = matrix

        self._calculate_matrix_evaluators_average()

        if self.average_counter > 0:
            self.average_note /= self.average_counter

            self._check_matrix_divergence()

    # get all notes and call _add_to_average to perform the average calc
    def _calculate_matrix_evaluators_average(self):
        for matrix_type in self.matrix:
            for evaluator_name in self.matrix[matrix_type]:
                if isinstance(self.matrix[matrix_type][evaluator_name], dict):
                    for time_frame in self.matrix[matrix_type][evaluator_name]:
                        self._add_to_average(self.matrix[matrix_type][evaluator_name][time_frame])
                else:
                    self._add_to_average(self.matrix[matrix_type][evaluator_name])

    def _add_to_average(self, value):
        # Todo check evaluator pertinence
        self.average_note += value
        self.average_counter += 1

    # Will raise a warning if calc_evaluator_divergence detect a divergence > +- DIVERGENCE_THRESHOLD
    def _check_matrix_divergence(self):
        for matrix_type in self.matrix:
            for evaluator_name in self.matrix[matrix_type]:
                if isinstance(self.matrix[matrix_type][evaluator_name], dict):
                    for time_frame in self.matrix[matrix_type][evaluator_name]:
                        if check_valid_eval_note(
                                self.matrix[matrix_type][evaluator_name][time_frame]):
                            if self._calc_eval_note_divergence(self.matrix[matrix_type][evaluator_name][time_frame]) \
                                    is not START_PENDING_EVAL_NOTE:
                                self._log_divergence(matrix_type,
                                                     evaluator_name,
                                                     self.matrix[matrix_type][evaluator_name][time_frame],
                                                     time_frame)
                else:
                    if check_valid_eval_note(self.matrix[matrix_type][evaluator_name]):
                        if self._calc_eval_note_divergence(self.matrix[matrix_type][evaluator_name]) \
                                is not START_PENDING_EVAL_NOTE:
                            self._log_divergence(matrix_type,
                                                 evaluator_name,
                                                 self.matrix[matrix_type][evaluator_name])

    # Will be called to calculate localized divergence note calc for an evaluator name, for each time frame or a
    # specific one
    def calc_evaluator_divergence(self, matrix_type, evaluator_name, time_frame=None):
        if time_frame is not None:
            if check_valid_eval_note(self.matrix[matrix_type][evaluator_name][time_frame]):
                return self._calc_eval_note_divergence(self.matrix[matrix_type][evaluator_name][time_frame])
            else:
                return START_PENDING_EVAL_NOTE

        elif isinstance(self.matrix[matrix_type][evaluator_name], dict):
            local_divergence_average = 0
            local_divergence_counter = 0
            for time_frame_iteration in self.matrix[matrix_type][evaluator_name]:
                if check_valid_eval_note(self.matrix[matrix_type][evaluator_name][time_frame_iteration]):
                    result = self._calc_eval_note_divergence(self.matrix[matrix_type][evaluator_name]
                                                             [time_frame_iteration])
                    if result is not START_PENDING_EVAL_NOTE:
                        local_divergence_average += result
                        local_divergence_counter += 1

            if local_divergence_counter > 0:
                return local_divergence_average / local_divergence_counter
            else:
                return START_PENDING_EVAL_NOTE

        else:
            if check_valid_eval_note(self.matrix[matrix_type][evaluator_name]):
                return self._calc_eval_note_divergence(self.matrix[matrix_type][evaluator_name])
            else:
                return START_PENDING_EVAL_NOTE

    # check if the eval note is between average_note - DIVERGENCE_THRESHOLD and average_note + DIVERGENCE_THRESHOLD
    def _calc_eval_note_divergence(self, eval_note):
        if self.average_note <= 0:
            if self.average_note + self.DIVERGENCE_THRESHOLD < eval_note < self.average_note - self.DIVERGENCE_THRESHOLD:
                return START_PENDING_EVAL_NOTE
        else:
            if self.average_note + self.DIVERGENCE_THRESHOLD > eval_note > self.average_note - self.DIVERGENCE_THRESHOLD:
                return START_PENDING_EVAL_NOTE
        return eval_note

    def _log_divergence(self, matrix_type, evaluator_name, eval_note, time_frame=None):
        self.logger.warning("Divergence detected on {0} {1} {2} | Average : {3} -> Eval : {4} ".format(matrix_type,
                                                                                                       evaluator_name,
                                                                                                       time_frame,
                                                                                                       self.average_note,
                                                                                                       eval_note))
