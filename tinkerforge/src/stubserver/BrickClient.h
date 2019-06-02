/*
 * BrickClient.h
 *
 * Copyright (C) 2013 Holger Grosenick
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#ifndef BRICKCLIENT_H_
#define BRICKCLIENT_H_

#include "PacketTypes.h"

namespace stubserver {

/**
 * Basic interface which is used by {@link BrickStack} in order to send
 * back responses to the network connected clients.
 */
class BrickClient
{
public:
    BrickClient();
    virtual ~BrickClient();

    virtual bool sendResponse(const IOPacket& packet) = 0;
};

} /* namespace stubserver */

#endif /* BRICKCLIENT_H_ */