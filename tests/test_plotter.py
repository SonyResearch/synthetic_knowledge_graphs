import datetime
import os

import numpy as np
import pytest

from synthetic_knowledge_graphs.impl.plotter import MatplotlibPlotter


@pytest.mark.parametrize("device", ["cpu"])
@pytest.mark.parametrize("mode", ["show", "save"])
def test_matplotlib(device, mode):
    plotter = MatplotlibPlotter()
    figure = plotter.create_figure()
    axis = plotter.get_axis(figure)
    if mode == "save":
        folder = os.path.join("tests", "images")
        # Create folder if it doesn't exist
        if not os.path.exists(folder):
            os.makedirs(folder)

        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f"test_matplotlib_{timestamp}.png"

        file_path = os.path.join(folder, file_name)
        axis.plot(np.random.rand(10))
        plotter.save(figure, file_path)
        assert os.path.exists(file_path)
        # Clean up
        os.remove(file_path)

    elif mode == "show":
        axis.plot(np.random.rand(10))
        plotter.show(figure)

    plotter.close(figure)
