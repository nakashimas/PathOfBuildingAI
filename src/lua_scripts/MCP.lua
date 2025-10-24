local json = require("dkjson")

local t_insert = table.insert
local FRAME_INTERVAL = 30
local requestPath = os.getenv("POB_AI_REQUEST") or "./temp/request.json"
local responsePath = os.getenv("POB_AI_RESPONSE") or "./temp/response.json"
local lastModified = nil

LoadModule("Modules/BuildSiteTools")
Build = LoadModule("Modules/Build.lua")

MCP = {}

local getExportSiteFromImportList = function(urlText)
    for j=1,#buildSites.websiteList do
        if urlText:match(buildSites.websiteList[j].matchURL) then
            return buildSites.websiteList[j]
        end
    end
end

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
    local isSuccess, response = pcall(MCP.execute, req)

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
    elseif req.command == "downloadBuild" then
		buildSites.DownloadBuild(
            req.link,
            getExportSiteFromImportList(req.link),
            function(isSuccess, data, importLink)
                if not isSuccess then
                    main:SetMode("BUILD", false, data)
                else
                    local xmlText = Inflate(common.base64.decode(data:gsub("-","+"):gsub("_","/")))
                    main:SetMode("BUILD", false, req.buildName or "Imported Build", xmlText, false, importLink)
                    main.newModeChangeToTree = true
                end
            end
        )
        response["status"] = 200
    elseif req.command == "uploadBuild" then
        local buildCode = common.base64.encode(Deflate(main.modes["BUILD"]:SaveDB("code"))):gsub("+","-"):gsub("/","_")
        response["code"] = buildCode
        response["url"] = "NA"
        response["status"] = 200
    elseif req.command == "getBuildFolder" then
        response["buildFolder"] = main.buildPath
        response["status"] = 200
    elseif req.command == "listItemBaseType" then
        local searchResultBaseTypes = {}
        for _, typeName in ipairs(main.modes["BUILD"].data.itemBaseTypeList) do
            t_insert(searchResultBaseTypes, typeName)
        end
        response["result"] = searchResultBaseTypes
        response["status"] = 200
    elseif req.command == "listItemBase" then
        local baseList = main.modes["BUILD"].data.itemBaseLists[req.type]
        local searchResultBases = {}
        for _, base in ipairs(baseList) do
            t_insert(searchResultBases, {
                name = base.name,
                type = typeName,
                implicit = base.base.implicit,
                tags = base.base.tags,
                reqs = base.base.req,
            })
        end
        response["result"] = searchResultBases
        response["status"] = 200
    elseif req.command == "listItemUniqueType" then
        local uniqueTypeList = main.modes["BUILD"].data.uniques
        local searchResultUniqueTypes = {}
        for name, _ in pairs(uniqueTypeList) do
            t_insert(searchResultUniqueTypes, name)
        end
        response["result"] = searchResultUniqueTypes
        response["status"] = 200
    elseif req.command == "listItemUnique" then
        local uniqueTypeList = main.modes["BUILD"].data.uniques
        local uniqueList = uniqueTypeList[req.type]
        local searchResultUniques = {}
        for _, raw in ipairs(uniqueList) do
            local item = new("Item", raw)
            item:BuildAndParseRaw()
            t_insert(searchResultUniques, {
                name = item.name,
                raw = raw,
                base = item.baseName,
                implicit = item.base.implicitModLines,
                explicit = item.explicitModLines,
                reqs = item.base.req,
                tags = item.base.tags,
                rarity = item.rarity,
            })
        end
        response["result"] = searchResultUniques
        response["status"] = 200
    elseif req.command == "listItem" then
        local itemList = main.modes["BUILD"].itemsTab.items
        local searchResultItems = {}
        for selItemId, item in pairs(itemList) do
            t_insert(searchResultItems, {
                itemId = selItemId,
                name = item.name,
                raw = item.raw,
                base = item.baseName,
                implicit = item.base.implicitModLines,
                -- explicit = item.explicitModLines,
                reqs = item.base.req,
                tags = item.base.tags,
                rarity = item.rarity,
            })
        end
        response["result"] = searchResultItems
        response["status"] = 200
    elseif req.command == "listItemSlot" then
        local slotList = main.modes["BUILD"].itemsTab.slots
        local searchResultSlots = {}
        for _, slot in pairs(slotList) do
            t_insert(searchResultSlots, {
                name = slot.slotName,
                active = slot:shown(),
                itemId = slot.selItemId,
            })
        end
        response["result"] = searchResultSlots
        response["status"] = 200
    elseif req.command == "setItemSlot" then
        local itemSetId = req.itemSetId or main.modes["BUILD"].itemsTab.activeItemSetId or 1
        local item = main.modes["BUILD"].itemsTab.items[req.itemId]
        main.modes["BUILD"].itemsTab:EquipItemInSet(item, itemSetId)
        response["status"] = 200
    elseif req.command == "addItem" then
        local item = new("Item", req.item.raw)
        item:BuildAndParseRaw()
        main.modes["BUILD"].itemsTab:AddItem(item, true)
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