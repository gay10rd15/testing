#include "c++lib/mylib.h"

namespace pause {
    void for_seconds(int seconds) {
        // Call the standard function correctly
        std::this_thread::sleep_for(std::chrono::seconds(seconds));
    }
}   