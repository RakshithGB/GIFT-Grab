#pragma once

#include "ivideosource.h"
#include "except.h"

namespace gg {

//!
//! \brief Lists supported framegrabber hardware
//!
enum Device {
    DVI2PCIeDuo
};

//!
//! \brief Used for connecting to supported
//! framegrabber hardware
//!
class Factory {
protected:
    //!
    //! \brief So that can keep track of everything
    //! opened and in use
    //!
    static IVideoSource * _sources[1];

public:
    //!
    //! \brief Try to connect to specified device
    //! \param type
    //! \return pointer to the device's framegrabber
    //! \throw DeviceNotFound if connection attempt
    //! fails
    //!
    static IVideoSource * connect(enum Device type);

    //!
    //! \brief Disconnect from specified \c type device,
    //! if already connected
    //! \param type
    //! \throw DeviceNotFound if \c type not recognised
    //! \sa connect - IVideoSource object \c connect
    //! returns will be destroyed by this, and hence the
    //! pointer unusable
    //!
    static void disconnect(enum Device type);
};

}
