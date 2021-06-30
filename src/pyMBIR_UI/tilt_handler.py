import numpy as np

from . import DataType
from .loader import Loader
from .utilities.get import Get
from . import TiltAlgorithm
from .tilt.direct_minimization import DirectMinimization


class TiltHandler:

    def __init__(self, parent=None):
        self.parent = parent

    def initialize_tilt_correction(self):
        list_image = self.parent.input['data'][DataType.projections]
        if list_image is None:
            return

        # file index
        first_image = list_image[0]
        nbr_files = len(self.parent.input['list files'][DataType.projections])
        self.parent.ui.tilt_correction_file_index_horizontalSlider.setMaximum(nbr_files-1)
        image_height, image_width = np.shape(first_image)
        self.parent.tilt_correction_image_height = image_height
        self.parent.tilt_correction_image_width = image_width

        self.file_index_changed()

    def file_index_changed(self):
        file_index_selected = self.parent.ui.tilt_correction_file_index_horizontalSlider.value()
        o_loader = Loader(parent=self.parent)
        image = o_loader.retrieve_data(file_index=file_index_selected)
        transpose_image = np.transpose(image)
        self.parent.tilt_correction_image_view.setImage(transpose_image)

    def master_checkBox_clicked(self):
        master_value = self.parent.ui.tilt_correction_checkBox.isChecked()
        self.parent.ui.tilt_correction_frame.setEnabled(master_value)

    def correction_algorithm_changed(self):
        o_get = Get(parent=self.parent)
        algo_selected = o_get.tilt_algorithm_selected()
        if algo_selected == TiltAlgorithm.direct_minimization:
            self.direct_minimization()
        elif algo_selected == TiltAlgorithm.phase_correlation:
            self.phase_correlation()
        elif algo_selected == TiltAlgorithm.use_center:
            self.use_center()

    def direct_minimization(self):
        o_direct = DirectMinimization()
        tilt_value = o_direct.run()

    def phase_correlation(self):
        pass

    def use_center(self):
        pass
