{ config, pkgs, lib, ... }:

with lib;

let
  cfg = config.services.eSquid;
in
{
  options = {
    services.eSquid = {
      enable = mkOption {
        type = types.bool;
        default = false;
        description = ''
          Enable the eSquid Discord bot.
        '';
      };

      token = mkOption {
        type = types.str;
        example = literalExpression "XXXXXXXXXXXXXXXXXXXXXXXX.XXXXXX.XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX";
        description = ''
          The token for the Discord bot account.
          If you do not have this, you can get it from https://discord.com/developers.
        '';
      };

      dataDir = mkOption {
        type = types.path;
        default = "/srv/esquid";
        example = literalExpression "/srv/esquid";
        description = ''
          Location where eSquid will store its data.
          This will also be where the token, admin ids, and default guild will be stored.
        '';
      };

      botAdminIDs = mkOption {
        type = types.listOf (types.strMatching ''^([0-9]*)$'');
        default = [""];
        example = literalExpression "[ 135935815825096705 1085405405972279336]";
        description = ''
          Discord IDs of users that can run more dangerous commands such as unload.
          Only put IDs of people you want to have complete control over the bot.
        '';
      };

      testingGuild = mkOption {
        type = types.strMatching ''^([0-9]*)$'';
        default = "";
        example = literalExpression "375409834197123092";
        description = ''
          The default guild determines which Discord server will recieve app commands first.
          This is usually a testing server.
        '';
      };

      package = mkOption {
        type = types.package;
        default = pkgs.esquid;
        example = literalExpression "pkgs.esquid";
      };
    };
  };

  config = mkIf cfg.enable {
    users = {
      users.esquid = {
        description = "eSquid Discord bot service user";
        home = cfg.dataDir;
        isSystemUser = true;
        group = "esquid";
      };
      groups.esquid = { };
    };

    system.activationScripts.esquidData.text = ''
      mkdir -p ${cfg.dataDir}
      chown esquid:esquid ${cfg.dataDir}
      chmod -R 760 ${cfg.dataDir}
    '';

    systemd.services.esquid = {
      enable = cfg.enable;
      after = [ "network.target" ];
      description = "eSquid Discord bot";
      environment = {
        ESQUID_ADMINS = strings.concatStrings (strings.intersperse "," cfg.botAdminIDs);
        ESQUID_DATA_DIR = cfg.dataDir;
        ESQUID_TESTING_GUILD = cfg.testingGuild;
        ESQUID_TOKEN = cfg.token;
      };
      preStart = ''
        mkdir -p ${cfg.dataDir}
      '';
      serviceConfig = {
        ExecStart = "${cfg.package}/bin/esquid";
        Restart = "always";
        User = "esquid";
      };
      wantedBy = [ "multi-user.target" ];
    };
  };
}
