local json = require("dkjson")

local t_insert = table.insert
local FRAME_INTERVAL = 30
local requestPath = os.getenv("POB_AI_REQUEST")
local responsePath = os.getenv("POB_AI_RESPONSE")
local lastModified = nil

Build = LoadModule("Modules/Build.lua")

MCP = {}

function getFileSignature(path)
    local f = io.open(path, "rb")
    if not f then return nil end
    local size = f:seek("end")
    f:seek("set", math.max(0, size - 256))  -- last 256
    local tail = f:read("*a") or ""
    f:close()
    
    local hash = 0
    for i = 1, #tail do
        hash = (hash + tail:byte(i)) % 65536
    end

    return size .. ":" .. hash
end

function MCP.startServer()
    MCP.frameCount = 0
    MCP.queue = {}

    main.onFrameFuncs["MPCListenServer"] = MCP.listenServer
    t_insert(main.toastMessages, "MPC Server Started.")
end

function MCP.listenServer()
    -- Pollings
    MCP.frameCount = MCP.frameCount + 1
    if MCP.frameCount % FRAME_INTERVAL ~= 0 then return end
    
    local modified = getFileSignature(requestPath)
    if not modified or modified == lastModified then return end
    
    -- Input Commands
    lastModified = modified
    local file = io.open(requestPath, "r")
    if not file then return end

    local content = file:read("*a")
    file:close()

    local ok, req = pcall(json.decode, content)
    if not ok or not req then return end

    -- Executions
    isSuccess, response = pcall(MCP.execute, req)

    if not isSuccess then
        local errorResponse = {}
        errorResponse["error"] = response
        MCP.respond(errorResponse)
    end
end

function MCP.execute(req)
    local response = {}

    if req.command == "loadBuild" then
        main:SetMode("BUILD", req.fileName, req.buildName)
        response["status"] = 200
    elseif req.command == "saveBuild" then
        main.modes["BUILD"].dbFileName = req.fileName
        main.modes["BUILD"].buildName = req.buildName
        main.modes["BUILD"].dbFileSubPath = req.fileSubPath or ""
        main.modes["BUILD"]:SaveDBFile()
        response["status"] = 200
    end

    MCP.respond(response)
    return response
end

function MCP.respond(obj)
    local file = io.open(responsePath, "w")
    if file then
        -- HASH randomize
        math.randomseed(os.time())
        obj["_rand"] = tostring(math.random())

        local content = json.encode(obj)
        
        file:write(content)
        file:close()
    end
end

return MCP