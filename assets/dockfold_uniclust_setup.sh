# ./script_name.sh /path/to/local/download/dir [gs://your-cloud-bucket]
LOCAL_DOWNLOAD_DIR=$1
CLOUD_BUCKET=$2

# Download Uniclust30
echo "Getting uniclust30..."
mkdir -p $LOCAL_DOWNLOAD_DIR
# Check if file already exists
if [ ! -f "$LOCAL_DOWNLOAD_DIR/uniclust30_2018_08_hhsuite.tar.gz" ]; then
    echo "Downloading uniclust30..."
    wget http://wwwuser.gwdg.de/~compbiol/uniclust/2018_08/uniclust30_2018_08_hhsuite.tar.gz -P $LOCAL_DOWNLOAD_DIR --no-check-certificate 
else
    echo "File already exists, skipping download."
fi
tar -zxvf $LOCAL_DOWNLOAD_DIR/uniclust30_2018_08_hhsuite.tar.gz -C $LOCAL_DOWNLOAD_DIR --strip-components=1
echo "Successfully processed uniclust30..."


# Function to check if gsutil is installed
function check_gsutil_installed {
    if ! command -v gsutil &> /dev/null
    then
        echo "gsutil could not be found, please install it to proceed upload to GCP bucket."
        exit 1
    fi
}

# Check if CLOUD_BUCKET is provided and starts with gs://
if [[ -n $CLOUD_BUCKET && $CLOUD_BUCKET == gs://* ]]; then
    check_gsutil_installed
    echo "Transferring downloaded file to cloud bucket: $CLOUD_BUCKET"
    gsutil -m cp -r $LOCAL_DOWNLOAD_DIR $CLOUD_BUCKET
    echo "Transfer completed."
else
    if [[ -n $CLOUD_BUCKET ]]; then
        echo "Error: Invalid cloud bucket name. It should start with gs://"
        exit 1
    fi
    echo "No cloud bucket specified, skipping upload."
fi


