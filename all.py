import pytest
import os
import time

if __name__ == '__main__':
    pytest.main()
    time.sleep(1)
    os.system("allure generate ./temps -o ./reports --clean")